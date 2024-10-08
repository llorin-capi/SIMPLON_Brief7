document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded');

    // Fonction pour défiler vers le haut de la page
    function scrollToTop() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Fonction pour gérer le rechargement de la page avec le bon nombre de participants
    function scrollToTopAndReload(url) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(function() {
            window.location.href = url;
        }, 500); // Délai pour permettre à la page de remonter avant le rechargement
    }

    // Gestionnaires pour les boutons de sélection de participants en haut
    document.getElementById('btn-16-top').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=16');
    });
    document.getElementById('btn-32-top').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=32');
    });
    document.getElementById('btn-64-top').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=64');
    });
    document.getElementById('btn-128-top').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=128');
    });

    // Gestionnaires pour les boutons de sélection de participants en bas
    document.getElementById('btn-16-bottom').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=16');
    });
    document.getElementById('btn-32-bottom').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=32');
    });
    document.getElementById('btn-64-bottom').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=64');
    });
    document.getElementById('btn-128-bottom').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=128');
    });
});
