document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded');

    // Fonction pour gérer le rechargement de la page avec le bon nombre de participants
    function scrollToTopAndReload(url) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(function() {
            window.location.href = url;
        }, 500); // Délai pour permettre à la page de remonter avant le rechargement
    }

    // Gestionnaires pour les boutons de sélection de participants en haut
    document.getElementById('btn-16-top').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=16'), stopFireworks;
    });
    document.getElementById('btn-32-top').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=32'), stopFireworks;
    });
    document.getElementById('btn-64-top').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=64'), stopFireworks;
    });
    document.getElementById('btn-128-top').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=128'), stopFireworks;
    });

    // Gestionnaires pour les boutons de sélection de participants en bas
    document.getElementById('btn-16-bottom').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=16'), stopFireworks;
    });
    document.getElementById('btn-32-bottom').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=32'), stopFireworks;
    });
    document.getElementById('btn-64-bottom').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=64'), stopFireworks;
    });
    document.getElementById('btn-128-bottom').addEventListener('click', function() {
        scrollToTopAndReload('/?participants=128'), stopFireworks;
    });
});

// Variable pour stocker l'ID du feu d'artifice en cours
var fireworksActive = false;
// Variable pour stocker si les feux d'artifice ont été arrêtés par un bouton
var fireworksStoppedByButton = false;

// Fonction qui lance les feux d'artifice
function launchFireworks() {
    if (fireworksStoppedByButton) return; // Si un bouton a arrêté le feu d'artifice, ne pas relancer

    fireworksActive = true; // Indique que les feux d'artifice sont actifs
    var duration = 2 * 1000; // Durée de 2 secondes
    var end = Date.now() + duration;
  
 (function frame() {
    if (!fireworksActive) return; // Si feux d'artifice arrêtés, sortir de la fonction

    confetti({
        particleCount: 3,
        angle: 60,
        spread: 15,
        origin: { x: 0 }
    });
    confetti({
        particleCount: 3,
        angle: 120,
        spread: 15,
        origin: { x: 1 }
    });
  
    if (Date.now() < end) {
        requestAnimationFrame(frame);
    }
    }());
}
  
// Fonction pour vérifier si on est en bas de la page
function isAtBottom() {
    return (window.innerHeight + window.scrollY) >= document.body.offsetHeight;
}

// Fonction pour arrêter le feu d'artifice
function stopFireworks() {
    fireworksActive = false; // Désactive les feux d'artifice
    fireworksStoppedByButton = true; // Indique qu'ils ont été stoppés par un bouton
}

// Détecte le défilement de la page
window.onscroll = function() {
    if (isAtBottom() && !fireworksActive && !fireworksStoppedByButton) {
        launchFireworks();
    }
  };
