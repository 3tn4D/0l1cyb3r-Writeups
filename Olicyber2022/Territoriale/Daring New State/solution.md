# Daring New State

## Enumerazione DNS

Per prima cosa analizziamo la zona DNS fornita dalla challenge.

Eseguiamo una query sulla zona `the.flag`:

```bash
dig @newstate.challs.olicyber.it -p 12008 root.the.flag +tcp
```

La query restituisce un `NXDOMAIN`, quindi `root.the.flag` non è un record valido. Tuttavia, nella sezione `AUTHORITY` troviamo informazioni sulla zona:

```text
the.flag. 86400 IN SOA ns1.the.flag. root.the.flag.
```

Continuiamo quindi cercando i nameserver autoritativi della zona.

---

## Ricerca del Name Server

Interroghiamo il record **NS** (*Name Server*):

```bash
dig @newstate.challs.olicyber.it -p 12008 the.flag NS +tcp
```

Otteniamo:

```text
the.flag. 86400 IN NS here.is.the.flag.
```

Il nameserver `here.is.the.flag` sembra essere un possibile punto di interesse.

---

## Analisi del record TXT

Cerchiamo eventuali informazioni nascoste nei record TXT:

```bash
dig @newstate.challs.olicyber.it -p 12008 here.is.the.flag TXT +tcp
```

Risultato:

```text
here.is.the.flag. 86400 IN TXT "flag{master_... look at the canonical name of base64decode.the.flag"
```

Il messaggio ci suggerisce di analizzare il **canonical name**, ovvero il record CNAME, di `base64decode.the.flag`.

---

## Analisi del CNAME

Eseguiamo la query:

```bash
dig @newstate.challs.olicyber.it -p 12008 base64decode.the.flag CNAME +tcp
```

Risultato:

```text
base64decode.the.flag. IN CNAME Li4ub2ZfZG5zXzw+fSByZXBsYWNlIDw+IHdpdGggaXAgb2YgZDgxODc3NmQ3.the.flag.
```

Il valore del CNAME contiene una stringa codificata in Base64.

Dopo la decodifica otteniamo:

```text
...of_dns_<>} replace <> with ip of d818776d7
```

Il messaggio indica di sostituire il placeholder `<>` con l'indirizzo IP associato all'host `d818776d7`.

---

## Risoluzione dell'IP

Cerchiamo il record A dell'host indicato:

```bash
dig @newstate.challs.olicyber.it -p 12008 d818776d7.the.flag A +tcp
```

Otteniamo:

```text
d818776d7.the.flag. 86400 IN A 127.254.13.25
```

L'indirizzo IP trovato è quindi:

```text
127.254.13.25
```

---

## Flag

Sostituendo il valore trovato nel template precedente otteniamo:

```text
flag{master_of_dns_127.254.13.25}
```