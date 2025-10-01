"""Views for Fan-Doom core app."""

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Follow, Author, Work, Post, Fandom, WikiPage, WorkFollow

@login_required
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = None
    if request.method == 'POST':
        print("Recibiendo POST request")
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        title = request.POST.get('title', '').strip()
        work_id = request.POST.get('work')
        print(f"Datos recibidos: content={content}, image={bool(image)}, title={title}, work_id={work_id}")
        author = Author.objects.filter(user=request.user).first()
        print(f"Author encontrado: {author}")
        work = Work.objects.filter(id=work_id).first() if work_id else None
        print(f"Work encontrado: {work}")
        
        # Validar que haya al menos contenido o imagen (no puede ser null)
        has_content = bool(content.strip() if content else False)
        has_image = bool(image)
        print(f"Tiene contenido: {has_content}, Tiene imagen: {has_image}")

        if not has_content and not has_image:
            error = 'La publicación debe tener texto o imagen (no puede estar vacía).'
            print("Error: Post vacío")
        elif not title:
            error = 'Debes ingresar un título para la publicación.'
            print("Error: Sin título")
        elif not author:
            error = 'No tienes permisos de autor para publicar.'
            print("Error: No es autor")
        elif not work:
            error = 'Debes seleccionar una obra.'
            print("Error: Sin obra seleccionada")
        else:
            print("Intentando crear el post...")
            post = Post(title=title, content=content, image=image, author=author, work=work)
            try:
                print("Validando post...")
                post.full_clean()
                print("Guardando post...")
                post.save()
                print("Post guardado exitosamente!")
                return redirect('home')
            except Exception as e:
                error = str(e)
                print(f"Error al guardar el post: {error}")
    
    posts = Post.objects.all().order_by('-created_at')
    seguidos = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
    autores_a_seguir = Author.objects.exclude(user__in=seguidos).exclude(user=request.user)[:6]
    total_autores = Author.objects.exclude(user__in=seguidos).exclude(user=request.user).count()
    seguidas_obras_ids = WorkFollow.objects.filter(user=request.user).values_list('work_id', flat=True)
    obras_a_seguir = Work.objects.exclude(id__in=seguidas_obras_ids)[:6]
    total_obras = Work.objects.exclude(id__in=seguidas_obras_ids).count()
    fandoms = Fandom.objects.all()
    works_followed = Work.objects.filter(id__in=seguidas_obras_ids)
    
    return render(request, 'core/home.html', {
        'posts': posts,
        'authors': autores_a_seguir,
        'fandoms': fandoms,
        'works': obras_a_seguir,
        'works_followed': works_followed,
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

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'core/post_detail.html', {'post': post})

def fandom_detail(request, fandom_id):
    fandom = get_object_or_404(Fandom, id=fandom_id)
    posts = Post.objects.filter(fandom=fandom)
    return render(request, 'core/fandom_detail.html', {
        'fandom': fandom,
        'posts': posts
    })

def wiki_page_detail(request, page_id):
    wiki_page = get_object_or_404(WikiPage, id=page_id)
    return render(request, 'core/wiki_page_detail.html', {'wiki_page': wiki_page})
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = None
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        image = request.FILES.get('image')
        title = request.POST.get('title', '').strip()
        work_id = request.POST.get('work')
        author = Author.objects.filter(user=request.user).first()
        work = Work.objects.filter(id=work_id).first() if work_id else None
        fandom = work.fandom if work and hasattr(work, 'fandom') else None
        if (not content and not image) or not title or not author or not work or not fandom:
            error = 'Debes ingresar título, texto o imagen, y seleccionar una obra que sigues.'
        else:
            post = Post(title=title, content=content, image=image, author=author, fandom=fandom)
            try:
                post.full_clean()
                post.save()
                return redirect('home')
            except Exception as e:
                error = str(e)
    posts = Post.objects.all().order_by('-created_at')
    # Autores a seguir (no mostrar si ya los sigue o es uno mismo)
    seguidos = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
    autores_a_seguir = Author.objects.exclude(user__in=seguidos).exclude(user=request.user)[:6]
    total_autores = Author.objects.exclude(user__in=seguidos).exclude(user=request.user).count()
    # Obras a seguir (no mostrar si ya las sigue)
    seguidas_obras_ids = WorkFollow.objects.filter(user=request.user).values_list('work_id', flat=True)
    obras_a_seguir = Work.objects.exclude(id__in=seguidas_obras_ids)[:6]
    total_obras = Work.objects.exclude(id__in=seguidas_obras_ids).count()
    fandoms = Fandom.objects.all()
    # Obras que el usuario sigue
    works_followed = Work.objects.filter(id__in=seguidas_obras_ids)
    return render(request, 'core/home.html', {
        'posts': posts,
        'authors': autores_a_seguir,
        'fandoms': fandoms,
        'works': obras_a_seguir,
        'works_followed': works_followed,
        'error': error,
        'total_autores': total_autores,
        'total_obras': total_obras
    })

"""Views for Fan-Doom core app."""
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Follow, Author, Work, Post, Fandom, WikiPage, WorkFollow

# Endpoint para seguir autores
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

# Endpoint para seguir obras
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
    # ...existing code...
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
def author_work_register(request):
    author = Author.objects.filter(user=request.user).first()
    if not author:
        return redirect('home')
    if request.method == 'POST':
        work_title = request.POST.get('work_title', '').strip()
        work_description = request.POST.get('work_description', '').strip()
        accept_integrity = request.POST.get('accept_integrity')
        if not work_title or not work_description or not accept_integrity:
            return render(request, 'core/author_work_register.html', {'error': 'Debes completar todos los campos y aceptar el aviso.'})
        # Guardar en el campo bio del autor
        author.bio = f"Obra: {work_title}\n\nDescripción: {work_description}"
        author.save()
        # Registrar la obra en la base de datos
        Work.objects.create(author=author, title=work_title, description=work_description)
        return redirect('home')
    return render(request, 'core/author_work_register.html')
def fandom_detail(request, fandom_id):
    fandom = get_object_or_404(Fandom, id=fandom_id)
    posts = Post.objects.filter(fandom=fandom)
    return render(request, 'core/fandom_detail.html', {'fandom': fandom, 'posts': posts})

def wiki_page_detail(request, page_id):
    wiki_page = get_object_or_404(WikiPage, id=page_id)
    return render(request, 'core/wiki_page_detail.html', {'wiki_page': wiki_page})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
