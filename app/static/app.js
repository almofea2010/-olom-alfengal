document.querySelectorAll('.copy-button').forEach((button) => {
  button.addEventListener('click', async () => {
    await navigator.clipboard.writeText(button.dataset.copy);
    const original = button.textContent;
    button.textContent = 'تم النسخ ✓';
    setTimeout(() => { button.textContent = original; }, 1600);
  });
});

let deferredInstallPrompt;
const installButton = document.querySelector('#install-button');
const imageInput = document.querySelector('#post-images');
const imagePreview = document.querySelector('#image-preview');
const imageData = document.querySelector('#image-data');

imageInput?.addEventListener('change', () => {
  if (!imagePreview) return;
  imagePreview.replaceChildren();
  if (imageData) imageData.value = '';

  Array.from(imageInput.files || []).forEach((file, index) => {
    if (!file.type.startsWith('image/')) return;
    const image = document.createElement('img');
    const previewUrl = URL.createObjectURL(file);
    image.src = previewUrl;
    image.alt = file.name;
    imagePreview.appendChild(image);

    if (index === 0 && imageData) {
      const reader = new FileReader();
      reader.addEventListener('load', () => { imageData.value = reader.result; });
      reader.readAsDataURL(file);
    }
  });
});

window.addEventListener('beforeinstallprompt', (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  if (installButton) installButton.hidden = false;
});

installButton?.addEventListener('click', async () => {
  if (!deferredInstallPrompt) return;
  deferredInstallPrompt.prompt();
  await deferredInstallPrompt.userChoice;
  deferredInstallPrompt = null;
  installButton.hidden = true;
});

window.addEventListener('appinstalled', () => {
  if (installButton) installButton.hidden = true;
});

document.querySelector('#prepare-post')?.addEventListener('click', () => {
  const idea = document.querySelector('#idea')?.value.trim();
  const mood = document.querySelector('input[name="mood"]:checked')?.value || 'بدون تحديد';
  const cafe = document.querySelector('#cafe_name')?.value.trim() || 'بدون تحديد';
  const tone = document.querySelector('#tone')?.value || 'بدون تحديد';
  const summary = document.querySelector('#post-summary');

  if (!summary) return;
  if (!idea) {
    summary.innerHTML = '<div class="empty-icon">!</div><h2>اكتب فكرة البوست أولاً</h2><p>أضف فكرة قصيرة حتى نجهز لك ملخص البوست.</p>';
    return;
  }

  summary.innerHTML = `<div class="empty-icon">✓</div><h2>البوست جاهز للتنفيذ</h2><div class="prepared-details"><p><strong>الفكرة:</strong> ${escapeHtml(idea)}</p><p><strong>الجو:</strong> ${escapeHtml(mood)}</p><p><strong>الكافيه:</strong> ${escapeHtml(cafe)}</p><p><strong>الأسلوب:</strong> ${escapeHtml(tone)}</p></div>`;
});

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[character]));
}
