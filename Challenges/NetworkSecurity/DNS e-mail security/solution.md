# DNS e record DNS

## Cos'è il DNS?

Il **DNS (Domain Name System)** è la "rubrica" di Internet.

Noi ricordiamo nomi come:

```text
google.com
```

ma i computer comunicano tramite indirizzi IP, ad esempio:

```text
142.250.184.14
```

Quando scriviamo `google.com` nel browser, il computer chiede a un server DNS:

> "Qual è l'indirizzo IP di `google.com`?"

Il server DNS risponde consultando i **record DNS** del dominio.

---

# Cosa sono i record DNS?

Un dominio contiene diversi record, ognuno con uno scopo specifico.

Si può immaginare un dominio come una cartella:

```text
example.com
│
├── A
├── AAAA
├── MX
├── TXT
├── NS
├── CNAME
└── ...
```

Ogni record rappresenta un'informazione diversa.

## Record A

Associa un nome di dominio a un indirizzo IPv4.

Esempio:

```text
google.com

A

142.250.184.14
```

Con il comando:

```bash
dig google.com A
```

si ottiene l'indirizzo IPv4 del dominio.

---

## Record AAAA

È equivalente al record A, ma contiene un indirizzo IPv6.

Esempio:

```text
google.com

AAAA

2a00:1450:4002::200e
```

---

## Record MX (Mail Exchange)

Specifica quali server ricevono la posta elettronica per un dominio.

Esempio:

```text
example.com

MX

10 mail.example.com
```

Quando si invia una mail a:

```text
utente@example.com
```

il server consulta il record MX di `example.com` per sapere a quale server consegnarla.

---

## Record TXT

Contiene testo libero.

Può essere usato per molti scopi.

Esempio semplice:

```text
example.com

TXT

"ciao"
```

Oppure per SPF:

```text
example.com

TXT

"v=spf1 include:_spf.example.com -all"
```

SPF, DKIM e DMARC utilizzano principalmente record TXT.

---

## Record NS

Indica quali server DNS sono autorevoli per un dominio.

Esempio:

```text
example.com

NS

ns1.example.com
```

---

## Record CNAME

Definisce un alias.

Esempio:

```text
www.example.com

CNAME

example.com
```

Significa che `www.example.com` punta allo stesso host di `example.com`.

---

# Il comando `dig`

`dig` significa **Domain Information Groper** ed è uno strumento per interrogare direttamente un server DNS.

Ad esempio:

```bash
dig google.com A
```

chiede:

> "Dammi il record A di `google.com`."

Oppure:

```bash
dig google.com MX
```

chiede:

> "Dammi i record MX."

Oppure:

```bash
dig google.com TXT
```

chiede:

> "Dammi i record TXT."

---

# Il simbolo `@`

Normalmente `dig` utilizza il server DNS configurato nel sistema operativo.

Con:

```bash
dig @8.8.8.8 google.com
```

si specifica invece quale server DNS interrogare.

In questo caso viene interrogato il DNS pubblico di Google (`8.8.8.8`).

---

# Analisi del comando della challenge

```bash
dig -p10502 @emailsec.challs.olicyber.it _spf.mail.dns-email.localhost TXT
```

Vediamo ogni parte:

- `dig` → esegue una query DNS.
- `-p10502` → utilizza la porta **10502** invece della porta DNS standard (53). Nelle CTF è comune usare porte diverse.
- `@emailsec.challs.olicyber.it` → indica il server DNS della challenge da interrogare.
- `_spf.mail.dns-email.localhost` → è il nome del dominio da cercare.
- `TXT` → richiede il record DNS di tipo TXT.

In pratica il comando significa:

> "Chiedi al server DNS della challenge il record TXT associato al dominio `_spf.mail.dns-email.localhost`."

---

# Cos'è `_spf`?

Dal punto di vista del DNS **non ha alcun significato speciale**.

È semplicemente un nome di dominio, come potrebbero esserlo:

```text
server.example.com
```

oppure

```text
mail.example.com
```

La differenza è che, per convenzione, gli amministratori usano `_spf` per contenere informazioni relative a **SPF (Sender Policy Framework)**.

Ad esempio:

```text
example.com
│
├── TXT "v=spf1 include:_spf.example.com -all"
│
└── _spf.example.com
    TXT "v=spf1 ip4:10.0.0.1 ip4:10.0.0.2 ~all"
```

Il record principale rimane piccolo e può includere altri record SPF tramite il meccanismo `include:`.

---

# Perché c'è il carattere `_`?

L'underscore (`_`) è una **convenzione**.

Serve a indicare che quel nome **non rappresenta un host** (cioè un computer raggiungibile in rete), ma contiene informazioni utilizzate da un protocollo.

Altri esempi molto comuni sono:

```text
_dmarc.example.com
```

Contiene la politica DMARC.

```text
_domainkey.example.com
```

Contiene le chiavi DKIM.

```text
_acme-challenge.example.com
```

Utilizzato da Let's Encrypt per verificare il possesso del dominio.

```text
_sip._tcp.example.com
```

Utilizzato dai servizi SIP tramite record SRV.

Questi nomi non identificano macchine, ma informazioni usate da protocolli specifici.

---

# Come leggere `_spf.mail.dns-email.localhost`

I nomi DNS si leggono da destra verso sinistra:

```text
_spf.mail.dns-email.localhost
│    │       │
│    │       └── dominio principale
│    └────────── sottodominio "mail"
└─────────────── nodo dedicato alle informazioni SPF
```

---

# Un'analogia

Si può immaginare il DNS come un archivio di cartelle.

```text
dns-email.localhost
│
├── A
├── MX
├── TXT
│
└── mail
    │
    ├── A
    ├── MX
    ├── TXT
    │
    └── _spf
        │
        └── TXT
```

Quando si esegue:

```bash
dig _spf.mail.dns-email.localhost TXT
```

si sta chiedendo al server DNS:

> "Apri il dominio `dns-email.localhost`, entra nel sottodominio `mail`, poi nel nodo `_spf` e mostrami il record di tipo `TXT`."

Questo è esattamente ciò che fanno anche i server di posta quando verificano le politiche SPF di un dominio.

***

# Soluzione della challenge

L'obiettivo della challenge è seguire le informazioni presenti nei record DNS fino a trovare la flag.

---

## 1. Individuare il server di posta (record MX)

Per prima cosa si interroga il record **MX** del dominio:

```bash
dig -p10502 @emailsec.challs.olicyber.it dns-email.localhost MX
```

Output rilevante:

```text
dns-email.localhost.    IN MX 10 mail.dns-email.localhost.
```

### Cosa significa?

Il record **MX** indica quale server gestisce la posta elettronica del dominio.

In questo caso il server di posta è:

```text
mail.dns-email.localhost
```

Poiché la challenge riguarda la sicurezza delle email (SPF), è naturale continuare l'analisi su questo host.

---

## 2. Cercare il record SPF

Per convenzione i record SPF vengono spesso salvati in un sottodominio chiamato `_spf`.

Si interroga quindi il record TXT:

```bash
dig -p10502 @emailsec.challs.olicyber.it _spf.mail.dns-email.localhost TXT
```

Output rilevante:

```text
v=spf1 include:_netblocks.mail.dns-email.localhost.
```

### Cosa significa?

Il record SPF non contiene direttamente gli indirizzi autorizzati, ma utilizza la direttiva:

```text
include:_netblocks.mail.dns-email.localhost
```

Questo significa:

> "Per completare la configurazione SPF bisogna consultare anche il dominio `_netblocks.mail.dns-email.localhost`."

Per questo motivo bisogna effettuare un'altra query DNS.

---

## 3. Seguire l'`include`

Si interroga quindi il dominio indicato dal record SPF:

```bash
dig -p10502 @emailsec.challs.olicyber.it _netblocks.mail.dns-email.localhost
```

Output rilevante:

```text
_netblocks.mail.dns-email.localhost. IN CNAME flag{dNs_15_fuLl_0f_qu35t!On5}.dns-email.localhost.
```

### Cosa significa?

Il server DNS risponde con un record **CNAME**, cioè un alias.

Normalmente un record CNAME punta a un altro nome di dominio.

In questo caso, invece, il nome del dominio di destinazione contiene direttamente la flag:

```text
flag{dNs_15_fuLl_0f_qu35t!On5}
```

---

# Flag

```text
flag{dNs_15_fuLl_0f_qu35t!On5}
```

---

# Riassunto del percorso

```text
dns-email.localhost
        │
        ▼
      Record MX
        │
        ▼
mail.dns-email.localhost
        │
        ▼
_spf.mail.dns-email.localhost
        │
        ▼
include:_netblocks.mail.dns-email.localhost
        │
        ▼
CNAME
        │
        ▼
flag{dNs_15_fuLl_0f_qu35t!On5}.dns-email.localhost
```

La challenge consiste quindi nel seguire la catena di record DNS (MX → TXT/SPF → include → CNAME) fino a raggiungere il dominio che contiene la flag.