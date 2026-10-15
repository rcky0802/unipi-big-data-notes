# Appunti di Information Retrieval

> 📍 *Parte dell'hub documentale unificato degli appunti universitari: [Visualizza Hub Principale](../README.md)*

Appunti universitari in LaTeX per il corso di **Information Retrieval** (Anno Accademico 2026/2027), strutturati in capitoli modulari e compilabili sia tramite Docker sia in ambiente locale.

## Prerequisiti

Per la compilazione locale sono consigliati:
1. [Visual Studio Code](https://code.visualstudio.com/) con estensione [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop)
2. Una distribuzione LaTeX (es. [MiKTeX](https://miktex.org/download) su Windows con `latexmk`)
3. Oppure semplicemente [Docker Desktop](https://www.docker.com/products/docker-desktop) sfruttando il container unificato del repository.

## Compilazione

Dalla radice del repository è possibile compilare la dispensa con lo script unificato PowerShell:

```powershell
# Compila la dispensa in italiano
.\scripts\build.ps1 -Subject "Information-Retrieval"
```

Oppure direttamente all'interno della cartella `Information-Retrieval` con `latexmk`:

```powershell
latexmk -pdf -interaction=nonstopmode main_it.tex
```

Per rimuovere i file ausiliari di compilazione:

```powershell
latexmk -c
```

## Struttura della Cartella e Indice dei Capitoli

- **Capitolo 0: Introduzione e Architettura dell'Information Retrieval** (`00`)
  - Definizioni e motivazioni dell'IR, confronto IR vs. Data Retrieval (SQL/DBMS).
  - I due obiettivi fondamentali: Efficacia (*Effectiveness*) vs. Efficienza (*Efficiency*) (pipelining, hazard, gerarchia di memoria, SIMD, calcolo parallelo).
  - Proprietà del linguaggio naturale (legge di Zipf, legge di Heaps), pipeline di text preprocessing.
  - Struttura dell'Inverted Index: dizionario + posting list, algoritmo di Merge Intersection.
  - Compressione dell'indice: Binary Interpolative Coding (partizionamento ricorsivo con mediana), codifica a dizionario LZ77.
  - Neural Information Retrieval: Interaction-based (Cross-Encoder) vs. Representation-based (Bi-Encoder).
  - Famiglie di embedding: Dense single-vector, Dense multi-vector (ColBERT late interaction / MaxSim), Sparse single-vector (SPLADE).
  - Ricerca approssimata dei primi $k$ vicini ($k$-ANN, MIPS, TusKANNy).

- **Capitolo 1: Valutazione dei Sistemi di Information Retrieval** (`01`)
  - Valutazione della qualità di ricerca: efficienza, servizi accessori ed efficacia intrinseca.
  - Misurare la soddisfazione dell'utente: CTR, ricerche a zero clic, conversioni, fidelizzazione, Dwell Time e impatto degli LLM.
  - Il Paradigma di Cranfield (Cyril Cleverdon), collezioni di test benchmark (corpus, query, qrel).
  - Sfide di scala combinatoria, trade-off del crowdsourcing, infrastruttura TREC.
  - La tecnica di Pooling, assunzioni sui documenti non giudicati e pooling bias.
  - Bisogno informativo (*information need*) vs. query superficiale.
  - Valutazione non ordinata (tabelle di contingenza, Precisione, Richiamo, media armonica $F_1$, $F_\beta$ pesata).
  - Valutazione ordinata (Precision@k, Recall@k, Average Precision, macro-averaging MAP, MRR per ricerche known-item).

- **Capitolo 2: Efficienza su Architetture CPU Moderne** (`02`)
  - Gerarchia di memoria (L1/L2/L3/RAM), linee di cache, località spaziale/temporale, prefetcher hardware.
  - Scansione sequenziale vs. pointer-chasing: benchmark in Rust e salti allineati alle cache line.
  - Pipeline a 5 stadi, latenza vs. throughput, esecuzione superscalare e porte di esecuzione.
  - Hazard strutturali, data hazard RAW e interleaving di catene di dipendenza.
  - Control hazard, esecuzione speculativa, costo del branch misprediction e tecniche branchless.

- **Capitolo 3: Natural Language Processing e Preprocessing del Testo** (`03`)
  - Riepilogo della valutazione con rilevanza graduata (CG, DCG e normalizzazione query-dipendente NDCG).
  - Caratteristiche del linguaggio naturale (ambiguità, conoscenza del mondo, deriva temporale) e legge di Zipf (principio del minimo sforzo, hapax legomena, trade-off sulle stop word).
  - Pipeline di web scraping con `urllib` e rimozione dei tag HTML con `BeautifulSoup`.
  - Pipeline di text preprocessing: tokenizzazione e disambiguazione dei confini di frase (`sent_tokenize`).
  - Normalizzazione morfologica: Stemming euristico (Porter) vs. Lemmatizzazione basata su sintassi (WordNet).
  - Rappresentazione Bag of Words (BoW) e perdita della semantica composizionale.
  - Arricchimento a livello subword e sequenziale: $n$-grammi di parole (ordine sintattico locale) e $n$-grammi di caratteri (tolleranza agli errori di battitura).

- **Capitolo 4: Modelli di Retrieval, Scoring e Ponderazione TF-IDF** (`04`)
  - Ricapitolazione del preprocessing ed evoluzione storica dell'IR (era statistica, era link analysis/PageRank, era neurale/ML).
  - Modello di retrieval booleano esatto, ambiti specialistici e patologia "feast or famine".
  - Fondamenti di Ranked Retrieval e query a testo libero.
  - Coefficiente di similarità di Jaccard, il paradosso di "Ides of March" e i tre limiti strutturali in IR.
  - Matrice termine-documento (incidenza binaria vs. frequenze assolute) e limiti dell'inversione sintattica nel Bag of Words.
  - Term Frequency sublineare logaritmica ($1 + \log_{10}(\text{tf})$), offset di continuità e curve di smorzamento.
  - Document Frequency ($df_t$) vs. Collection Frequency ($cf_t$), informativa dei termini e Inverse Document Frequency ($\text{idf}_t$).
  - Impatto dell'IDF su query a singolo termine vs. multi-termine.
  - Ponderazione composita TF-IDF e traccia dettagliata su lavagna ($N=806\,791$, ribilanciamento raw vs. log-TF).
  - Matrice di peso TF-IDF a valori reali in $\mathbb{R}^{|V|}$.

- **Capitolo 5: Vector Space Model (VSM), Notazione SMART e Okapi BM25** (`05`)
  - Fondamenti geometrici del Vector Space Model (VSM) ed estrema sparsità vettoriale.
  - Inadeguatezza della distanza euclidea in IR: esperimento dei documenti concatenati duplicati ($d' = d \circ d$) e direzione vs. magnitudine.
  - Cosine Similarity e normalizzazione vettoriale della lunghezza $L_2$ sull'ipersfera unitaria.
  - Architettura computazionale disaccoppiata offline/online nei motori di ricerca in produzione.
  - Caso di studio comparativo completo su romanzi classici (Jane Austen vs. Emily Brontë).
  - Tassonomia standard della notazione SMART (`ddd.qqq`), protocollo asimmetrico `lnc.ltc` e traccia d'esecuzione completa ($N=1\,000\,000$).
  - Scoring probabilistico Best Match 25 (Okapi BM25): saturazione asintotica della term frequency ($k_1$) e normalizzazione della lunghezza del documento ($b$).
  - Diagramma di flusso concettuale integrato: preprocessing, VSM, notazione SMART e BM25.

- **Capitolo 6: Architettura del Motore di Ricerca e Indicizzazione** (`06`)
  - Architettura di sistema: pipeline di ingestione/indicizzazione offline vs. elaborazione delle query online a bassa latenza ($< 50\text{--}100\text{ ms}$).
  - Paradigma Two-Stage Retrieval: estrazione candidati ad alto throughput (BM25 su posting list) seguito da re-ranking neurale (Learning-to-Rank / Transformer cross-encoder).
  - Formulazione del prodotto scalare come ponte tra retrieval lessicale classico e retrieval neurale denso.
  - Sparsità della matrice termine-documento ($> 99.99\%$ celle vuote) e confronto strutturale: Forward Index (orientato ai documenti) vs. Inverted Index (potatura statica orientata ai termini).
  - Layout fisico dell'indice invertito: dizionario residente in RAM, disaccoppiamento fisico tra stream monotoni di DocID (compressione $d$-gaps) e stream non ordinati di frequenze.
  - Trade-off ingegneristici: interi compressi vs. float precalcolati sotto vincoli di memoria.
  - Modelli ed estensioni di query: query di frase con indici posizionali, espansione di query, deriva semantica e stemming lessicale vs. espansione a runtime.

- **Capitolo 7: Elaborazione delle Query: Algoritmi di Scansione ed Efficienza con Skipping** (`07`)
  - Gerarchia statistica dell'indice invertito: dizionario residente in RAM ($df_t$, $F_t$) e posting list su memoria secondaria ($\langle \text{docID}, \text{tf} \rangle$).
  - Trade-off di sistema: motivazioni per cui i punteggi BM25 non sono precalcolati come float (compressione senza perdita, località dell'IDF in RAM, ranking agile a runtime).
  - Paradigmi di scansione: teoria formale di Term-at-a-Time (TAAT) vs. Document-at-a-Time (DAAT) con coda Min-Heap per i top-$k$ e schema architetturale TikZ.
  - Approfondimento operativo su TAAT: traccia d'esecuzione passo-passo, strutture accumulatori (DAT vs. Hash Table), cache miss hardware e impossibilità di skipping.
  - DAAT per query disgiuntive (OR) con fusione multi-puntatore in stile MergeSort ($\Theta(\sum |L_i|)$) e DAAT base per query congiuntive (AND).
  - Interfaccia a cursori sulle posting list: 5 primitive (`first_t`, `next_t`, `nextGEQ_t`, `docId_t`, `position_t`).
  - Limiti della ricerca esponenziale (Galloping Search) su flussi di bit compressi ($d$-gaps).
  - Partizionamento a blocchi industriali ($k=64/128$) e skip pointer: salto di blocchi compressi senza decompressione, codifica quasi-succinta Elias-Fano.
  - Algoritmi avanzati con `nextGEQ`: DAAT AND con skipping ottimizzato (traccia a 8 stadi) e TAAT AND ottimizzato con euristica Shortest-to-Longest (teorema e dimostrazione di riduzione monotona della cardinalità).
  - Applicazioni moderne nel retrieval neurale sparso (SPLADE), accelerazione hardware su GPU e vector search engine dedicati (Qdrant).
  - Tabella comparativa di sintesi finale: complessità computazionale, ingombro in RAM e capacità di skipping.

```text
Information-Retrieval/
├── assets/                 # Figure, grafici vettoriali e schemi TikZ
├── chapters/
│   └── it/                 # Capitoli in italiano (.tex)
├── config/
│   └── preamble_it.tex     # Preambolo e configurazione pacchetti
├── main_it.tex             # Entry point principale per la compilazione
├── main.tex                # Entry point per editor VS Code
├── references.bib          # Bibliografia
└── README.md               # Scheda descrittiva del corso
```

## Linee Guida per i Capitoli e le Figure

1. Ogni capitolo è un file autonomo incluso in `main_it.tex` tramite `\include{chapters/it/...}`.
2. Figure ed equazioni devono avere `\caption` descrittive e `\label` per la navigazione interna, richiamate nel testo con `\autoref{...}`.
3. Configurazioni globali, pacchetti e macro matematiche vanno collocati esclusivamente in `config/preamble_it.tex`.
