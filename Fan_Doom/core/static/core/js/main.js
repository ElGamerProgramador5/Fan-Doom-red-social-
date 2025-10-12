document.addEventListener('DOMContentLoaded', function() {
	var trigger = document.getElementById('trigger-post-form');
	var modalBg = document.getElementById('modal-bg');
	var closeBtn = document.getElementById('close-post-form');
	var form = document.getElementById('post-form');

	if (trigger && modalBg) {
		trigger.addEventListener('click', function() {
			// Reset form and show all fields for a new post
			if(form) {
				form.reset();
				let sharedInput = form.querySelector('input[name="shared_post_id"]');
				if (sharedInput) sharedInput.value = '';

				form.querySelector('select[name="work"]').style.display = 'block';
				form.querySelector('textarea[name="content"]').style.display = 'block';
				let imageInputContainer = form.querySelector('input[name="image"]');
				if(imageInputContainer) imageInputContainer.parentElement.parentElement.style.display = 'block';
			}

			modalBg.style.display = 'flex';
			setTimeout(function(){
				var input = form.querySelector('input[name="title"]');
				if(input) input.focus();
			}, 100);
		});
	}
	if (closeBtn && modalBg) {
		closeBtn.addEventListener('click', function(e) {
			e.preventDefault();
			modalBg.style.display = 'none';
		});
	}
	// Cerrar modal al hacer click fuera del formulario
	if (modalBg && form) {
		modalBg.addEventListener('click', function(e) {
			if (e.target === modalBg) {
				modalBg.style.display = 'none';
			}
		});
	}
});