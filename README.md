# model_pdf_generatorCtrl+C 
kill -9
lsof -i :5000
ps aux | grep postgres

Lorsque tu veux arrêter ton application Flask proprement, évite de forcer la fermeture du terminal. Utilise plutôt Ctrl+C dans le terminal où Flask est exécuté pour l’arrêter proprement. Cela libère le port sans avoir à tuer le processus manuellement.