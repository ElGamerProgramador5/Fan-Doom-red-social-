"""Views for Fan-Doom core app."""

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Follow, Author, Work, Post, Fandom, WikiPage, WorkFollow, Comment, Vote, Profile
from .forms import ProfileForm, WorkForm

@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = None
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        title = request.POST.get('title', '').strip()
        work_id = request.POST.get('work')
        shared_post_id = request.POST.get('shared_post_id')
        work = Work.objects.filter(id=work_id).first() if work_id else None
        
        has_content = bool(content.strip() if content else False)
        has_image = bool(image)

        if not has_content and not has_image and not shared_post_id:
            error = 'La publicación debe tener texto o imagen (no puede estar vacía).'
        elif not title:
            error = 'Debes ingresar un título para la publicación.'
        elif not work:
            error = 'Debes seleccionar una obra.'
        else:
            shared_post = None
            if shared_post_id:
                try:
                    shared_post = Post.objects.get(id=shared_post_id)
                except Post.DoesNotExist:
                    error = "El post que intentas compartir no existe."
            post = Post(title=title, content=content, image=image, user=request.user, work=work, shared_post=shared_post)
            try:
                post.full_clean()
                post.save()
                return redirect('home')
            except Exception as e:
                error = str(e)
    
    posts = Post.objects.all().order_by('-created_at')
    seguidos = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
    autores_a_seguir = Author.objects.exclude(user__in=seguidos).exclude(user=request.user)[:6]
    total_autores = Author.objects.exclude(user__in=seguidos).exclude(user=request.user).count()
    fandoms = Fandom.objects.all()

    # Exclude author's own works from 'works to follow' list
    seguidas_obras_ids = WorkFollow.objects.filter(user=request.user).values_list('work_id', flat=True)
    obras_a_seguir_query = Work.objects.exclude(id__in=seguidas_obras_ids)
    if hasattr(request.user, 'author'):
        obras_a_seguir_query = obras_a_seguir_query.exclude(author=request.user.author)
    obras_a_seguir = obras_a_seguir_query[:6]
    total_obras = obras_a_seguir_query.count()

    # Combine followed works and author's own works for the posting dropdown
    works_followed = Work.objects.filter(id__in=seguidas_obras_ids)
    works_for_posting = works_followed
    if hasattr(request.user, 'author'):
        authors_works = Work.objects.filter(author=request.user.author)
        works_for_posting = works_followed.union(authors_works).order_by('title')
    
    return render(request, 'core/home.html', {
        'posts': posts,
        'authors': autores_a_seguir,
        'fandoms': fandoms,
        'works': obras_a_seguir,
        'works_for_posting': works_for_posting,
        'error': error,
        'total_autores': total_autores,
        'total_obras': total_obras
    })

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Usuario o contraseña incorrectos.'
    return render(request, 'core/login.html', {'error': error})

def signup_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if User.objects.filter(username=username).exists():
            error = 'El usuario ya existe.'
        else:
            user = User.objects.create_user(username=username, password=password)
            if role == 'author':
                Author.objects.create(user=user)
                login(request, user)
                return redirect('author_work_register')
            else:
                login(request, user)
                return redirect('home')
    return render(request, 'core/signup.html', {'error': error})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
@require_POST
def follow_author(request):
    author_id = request.POST.get('author_id')
    if not author_id:
        return JsonResponse({'ok': False, 'error': 'ID inválido'})
    try:
        author = Author.objects.get(id=author_id)
        Follow.objects.get_or_create(follower=request.user, followed=author.user)
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})

@login_required
@require_POST
def follow_work(request):
    work_id = request.POST.get('work_id')
    if not work_id:
        return JsonResponse({'ok': False, 'error': 'ID inválido'})
    try:
        work = Work.objects.get(id=work_id)
        WorkFollow.objects.get_or_create(user=request.user, work=work)
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})

@login_required
def author_work_register(request):
    author = Author.objects.filter(user=request.user).first()
    if not author:
        return redirect('home')
    if request.method == 'POST':
        work_title = request.POST.get('work_title', '').strip()
        work_description = request.POST.get('work_description', '').strip()
        accept_integrity = request.POST.get('accept_integrity')
        if not work_title or not work_description or not accept_integrity:
            return render(request, 'core/author_work_register.html', {
                'error': 'Debes completar todos los campos y aceptar el aviso.'
            })
        # Guardar en el campo bio del autor
        author.bio = f"Obra: {work_title}\n\nDescripción: {work_description}"
        author.save()
        # Registrar la obra en la base de datos
        Work.objects.create(author=author, title=work_title, description=work_description)
        return redirect('home')
    return render(request, 'core/author_work_register.html')

@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    # Usamos get_or_create para asegurar que el perfil exista para usuarios antiguos.
    profile, created = Profile.objects.get_or_create(user=profile_user)
    user_posts = Post.objects.filter(user=profile_user).order_by('-created_at')
    
    context = {
        'profile_user': profile_user,
        'profile': profile,
        'posts': user_posts,
    }
    return render(request, 'core/profile.html', context)

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form
    }
    return render(request, 'core/edit_profile.html', context)


@login_required
def author_profile(request, username):
    author_user = get_object_or_404(User, username=username)
    author = get_object_or_404(Author, user=author_user)
    profile, created = Profile.objects.get_or_create(user=author_user)
    author_works = Work.objects.filter(author=author).order_by('-created_at')

    context = {
        'profile_user': author_user,
        'author': author,
        'profile': profile,
        'works': author_works,
    }
    return render(request, 'core/author_profile.html', context)


@login_required
def add_work(request):
    try:
        author = request.user.author
    except Author.DoesNotExist:
        return redirect('home') # Or show an error page

    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            work = form.save(commit=False)
            work.author = author
            work.save()
            return redirect('author_profile', username=request.user.username)
    else:
        form = WorkForm()

    context = {
        'form': form
    }
    return render(request, 'core/add_work.html', context)


@login_required
def edit_work(request, work_id):
    work = get_object_or_404(Work, id=work_id)

    # Security check: ensure the logged-in user is the author of the work
    if work.author.user != request.user:
        return redirect('home') # Or show a 403 Forbidden error

    if request.method == 'POST':
        form = WorkForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect('author_profile', username=request.user.username)
    else:
        form = WorkForm(instance=work)

    context = {
        'form': form,
        'work': work
    }
    return render(request, 'core/edit_work.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content and content.strip():
            Comment.objects.create(post=post, user=request.user, content=content)
            return redirect('post_detail', post_id=post.id)

    return render(request, 'core/post_detail.html', {'post': post, 'comments': comments})

def fandom_detail(request, fandom_id):
    fandom = get_object_or_404(Fandom, id=fandom_id)
    posts = Post.objects.filter(fandom=fandom)
    return render(request, 'core/fandom_detail.html', {
        'fandom': fandom,
        'posts': posts
    })

@login_required
@require_POST
def vote(request):
    post_id = request.POST.get('post_id')
    vote_type = request.POST.get('vote_type')

    if not post_id or not vote_type:
        return JsonResponse({'ok': False, 'error': 'ID de post y tipo de voto requeridos.'})

    try:
        post = Post.objects.get(id=post_id)
        vote_type = int(vote_type)

        if vote_type not in [Vote.UPVOTE, Vote.DOWNVOTE]:
            return JsonResponse({'ok': False, 'error': 'Tipo de voto inválido.'})

        vote, created = Vote.objects.get_or_create(
            user=request.user,
            post=post,
            defaults={'vote_type': vote_type}
        )

        if not created:
            if vote.vote_type == vote_type:
                # User is clicking the same button again, so remove the vote
                vote.delete()
            else:
                # User is changing their vote
                vote.vote_type = vote_type
                vote.save()
        
        return JsonResponse({
            'ok': True,
            'score': post.score,
            'postId': post.id
        })

    except Post.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Post no encontrado.'})
    except ValueError:
        return JsonResponse({'ok': False, 'error': 'Tipo de voto debe ser un número.'})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)})

def wiki_page_detail(request, page_id):
    wiki_page = get_object_or_404(WikiPage, id=page_id)
    return render(request, 'core/wiki_page_detail.html', {'wiki_page': wiki_page})