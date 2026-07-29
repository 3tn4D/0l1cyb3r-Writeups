# [crypto-1] Un po' di storia

Analizzando il riferimento temporale della pergamena, ovvero il XVI secolo, si può ricercare tra i cifrari storici utilizzati in quel periodo. Uno dei cifrari più famosi del 1500 è il **cifrario di Vigenère**, introdotto nel 1586.

La versione classica del cifrario di Vigenère però non produce un testo leggibile, quindi è necessario considerare alcune delle sue varianti.

Tra queste, quella corretta risulta essere l'**Autokey Cipher**, una variante del cifrario di Vigenère che utilizza una chiave iniziale e successivamente estende la chiave utilizzando il testo stesso (plaintext o ciphertext a seconda della variante).

Per procedere con la decrittazione è possibile utilizzare un tool automatico come **dCode**, selezionando il cifrario **Vigenère Autokey** e inserendo il testo cifrato.

Il risultato della decifratura fornisce il testo in chiaro, che deve solamente essere convertito nel formato richiesto per ottenere la flag finale.

```
flag{hai_rotto_autokey_bravo}
```

