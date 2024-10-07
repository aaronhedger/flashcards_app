def flashcard_algorithm(card_data, user_choices):
    rounds_to_reappear = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    max_cards_per_round = 9
    categorized_cards = {}
    card_reappear = {}
    total_cards = len(card_data)
    current_round = 1

    while True:
        current_round_cards = []

        # Ajouter des cartes qui doivent réapparaître ce round
        for index, next_round in list(card_reappear.items()):
            if next_round == current_round:
                current_round_cards.append(card_data[index - 1])  # Utiliser index pour accéder aux bonnes données

        # Ajouter des nouvelles cartes si moins de 9 cartes
        for card in card_data:
            if len(current_round_cards) >= max_cards_per_round:
                break
            if card['index'] not in card_reappear:
                current_round_cards.append(card)

        # Vérifier si toutes les cartes ont été catégorisées 'd' deux fois
        if len(current_round_cards) == 0:
            if all(categorized_cards.get(card, 0) >= 2 for card in range(1, total_cards + 1)):
                return []  # Terminer l'exercice
            else:
                current_round += 1  # Passer au round suivant si pas encore terminé
                continue  # Continuer la boucle pour le prochain round

        # Ici, le code pour traiter les choix utilisateur
        result = []
        for card in current_round_cards:
            card_id = card['index']
            choice = user_choices.get(card_id)

            # Ajouter la carte au résultat pour l'affichage
            result.append(card)

            # Calculer quand la carte doit réapparaître en fonction du choix
            if choice:
                reappear_round = current_round + rounds_to_reappear[choice]
                card_reappear[card_id] = reappear_round

                # Si 'd' est choisi, incrémenter le compteur de cette carte dans 'categorized_cards'
                if choice == 'd':
                    categorized_cards[card_id] = categorized_cards.get(card_id, 0) + 1

        current_round += 1
        return result  # Retourner les cartes à afficher