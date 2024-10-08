document.addEventListener('DOMContentLoaded', function() {
    console.log('Page loaded');

    // Fonction pour mettre à jour l'affichage du nombre de combattants
    function updateFighterCount(count) {
        document.getElementById('fighter-count-top').innerText = `Nombre de combattants sélectionnés : ${count}`;
        document.getElementById('fighter-count-bottom').innerText = `Nombre de combattants sélectionnés : ${count}`;
    }

    // Fonction pour obtenir la valeur des paramètres de l'URL
    function getURLParameter(name) {
        return new URLSearchParams(window.location.search).get(name);
    }

    // Fonction pour gérer l'effet de bouton sélectionné
    function handleButtonSelection(participants) {
        // Retirer la classe "selected" de tous les boutons
        const allButtons = document.querySelectorAll('button');
        allButtons.forEach(button => {
            button.classList.remove('selected');
        });

        // Ajouter la classe "selected" aux boutons correspondants en haut et en bas
        const topButton = document.getElementById(`btn-${participants}-top`);
        const bottomButton = document.getElementById(`btn-${participants}-bottom`);

        if (topButton) topButton.classList.add('selected');
        if (bottomButton) bottomButton.classList.add('selected');
    }

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

  
    // Récupération du paramètre 'participants' de l'URL
    const participants = getURLParameter('participants') || 8;  // Valeur par défaut : 8
    updateFighterCount(participants);

    // Appliquer la classe "selected" au bouton correspondant au chargement de la page
    handleButtonSelection(participants);

    // Fonction pour défiler vers le haut de la page avant de recharger
    function scrollToTopAndReload(url) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(function() {
            window.location.href = url;
        }, 500); // Délai pour permettre à la page de remonter avant le rechargement
    }

// Gestionnaires pour les boutons de sélection de participants en haut
document.getElementById('btn-8-top').addEventListener('click', function() {
    scrollToTopAndReload('/?participants=8'), stopFireworks;
});
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
document.getElementById('btn-8-bottom').addEventListener('click', function() {
    scrollToTopAndReload('/?participants=8'), stopFireworks;
});
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
})
