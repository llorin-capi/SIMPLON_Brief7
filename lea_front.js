document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded');

    // Gestionnaire pour le bouton de régénération
    const regenerateButton = document.getElementById('regenerate-button');
    regenerateButton.addEventListener('click', function() {
        // Remonter en haut de la page
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Après avoir remonté, recharger la page pour régénérer le tournoi
        setTimeout(function() {
            window.location.reload();
        }, 500); // Ajoute un délai pour permettre à la page de remonter avant le rechargement
    });
});