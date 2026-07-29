# Writeup: Firma dell'immagine "fish.jpg"

## Obiettivo
Ottenere una signature valida per `fish.jpg` senza farla firmare direttamente dal server.

## Il bug
Il server firma le immagini calcolandone l'hash **MD5**, ma nella verifica ignora i pixel del pesce. Basta quindi creare due immagini che mantengono i pixel originali delle immagini di partenza (fish e tiger) ma con **stesso MD5**: una la faccio firmare, l'altra la verifico con quella firma.

## Tool usato
[corkami/collisions](https://github.com/corkami/collisions/tree/master#png)

```bash
$ png.py fish.png tiger.png
```

Output:
- `collision1.png` → pixel di **fish**
- `collision2.png` → pixel di **tiger**

Stesso MD5, contenuto diverso.

## Passaggi
1. Carico `collision2.png` (tigre) in **"Firma opera"** → ottengo `signature.txt`.
2. Carico `collision1.png` (pesce) + `signature.txt` in **"Controlla firma"**.
3. Essendo lo stesso MD5, la verifica passa → **flag**.

## Perché funziona
MD5 è vulnerabile a collisioni: si possono costruire file diversi con lo stesso hash. Il server si fida solo dell'hash MD5, quindi non si accorge che l'immagine verificata è diversa da quella firmata.

## Fix
Usare un hash sicuro (es. SHA-256) e verificare tutta l'immagine, non basarsi solo sull'hash per la firma.