# E-mails d'échanges pour correctif et ajout d'une nouvelle fonctionnalité

Bonjour,

Je prends acte de vos remarques,  
effectivement je constate que l'application ne passe plus certains tests automatiques.

A première vue, certaines modifications apportées semblent causer une erreur de "_redirection_" sur la page de recommandation de produits alternatifs.  
Je vais investiguer là dessus et vous ferrai un premier retour d'ici demain soir.

De plus, effectivement la fonctionnalité de recherche en ligne est un point important pour l'expérience utilisateur.  
Une consultation en ligne de la base de données d'OpenFoodFacts sera effectuée  lorsque les informations stockées localement dans la base de données de l'application ne seront pas suffisantes pour répondre à la requête de l'utilisateur.

Cette nouvelle fonctionnalité, ainsi que les tests d'intégrations relatifs, seront réalisés en 3 jours après la résolution du problème principal de "_redirection_" de page.

Bien à vous

Mickaël TOUSSAINT

---

Bonjour,

Comme convenu le bug de "_redirection_" a été corrigé, tous les tests sont de nouveau exécutés avec succès.  
J'en ai profité pour refactorer le code relatif afin de le rendre plus lisible et modulaire.  
Les modifications associées sont consultables sur la révision ___86e458b___ du [dépôt git](https://github.com/MikodeSan/OpynFacts).

Je vous laisse prendre acte de la résolution du problème et revenir vers moi en cas de besoin.  
Sans retour de votre part sous une semaine, la correction apportée sera concidérée acceptée et validée.

Dans l'attente d'un éventuel retour, j'entame comme prévu la mise en oeuvre de la fonctionnalité de recherche de produit en ligne.

Bien à vous.

Mickaël TOUSSAINT

---

Bonjour,

Tout d'abord je suis content de votre retour positif sur la correction du bug,  
ce qui valide la remise en service du site internet.

Par ailleurs, je vous annonce la publication de la nouvelle fonctionnalité de recherche de produit par consultation de la base de données OpenFoodFacts.  
Vous pourrez constater sur le serveur de test, la validation des tests mis en place pour cette nouvelle fonctionnalité.  
De plus, vous pouvez également consulter sur le serveur d'alerte [Sentry](https://sentry.io/organizations/zwel-org/issues/?project=5392267), les notifications de recherches effectuées en ligne.

Comme d'habitude, je vous laisse prendre acte des modifications effectuées et revenir vers moi pour valider la solution mise en place.
Après validation de votre part au plus tard sous une semaine,
débutera la Vérification de Service Régulier pour une durée d'un mois.
Durant cette période toute anomalie remontée sur les modifications apportées sera corrigée.

Bien à vous.

Mickaël TOUSSAINT
