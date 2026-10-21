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
  - Metodologia e obiettivi: efficienza operativa (indicizzazione, latenza di query su 5M di documenti), servizi accessori (spell checking, snippet, raccomandazioni) ed efficacia intrinseca della SERP.
  - Misurare la soddisfazione dell'utente (*User Happiness*): CTR, zero-click searches, conversioni e spesa e-commerce, fidelizzazione e Dwell Time; riflessione critica nell'era dell'Agentic Search, turni conversazionali e RAG.
  - Il Paradigma di Cranfield (Cyril Cleverdon) e collezioni di test benchmark: tripletta formale $(\mathcal{D}, \mathcal{Q}, \mathcal{J})$, distinzione tra *Information Need* e query, esplosione combinatoria ($1/4$ di trilione di giudizi) e campionamento.
  - Metodologie di annotazione e query: campionamento da query log reali vs. formulazione manuale di esperti, crowdsourcing (Amazon Mechanical Turk, varianza statistica) e approcci LLM-as-a-Judge con relativi bias.
  - Evoluzione storica e framework TREC (NIST): corpora storici (Cranfield, Medline, OSHMED vs. TREC), struttura a tracce (*tracks*), definizione formale dei Topic (Title, Description, Narrative) e concetto di Run.
  - La tecnica del Pooling: campionamento dei top-$k$ da run eterogenee, deduplicazione nel pool $\mathcal{P}$, assunzione fondamentale di non rilevanza per i documenti *unpooled* e verifica empirica di stabilità.
  - Metriche binarie per insiemi non ordinati: matrice di contingenza $2 \times 2$, diagramma di Eulero-Venn, Precisione, Richiamo e loro trade-off intrinseco; media armonica $F_1$-score (proprietà analitiche contro la fallacia della media aritmetica) e misura pesata $F_\beta$ per domini precision-oriented ($\beta < 1$) o recall-oriented ($\beta > 1$, medico/brevettuale).
  - Metriche basate sul ranking (rilevanza binaria): $P@k$ ed evidenza del comportamento non monotono ($P@4 < P@3$), limite di $P@k$ nella media macro tra query eterogenee; Average Precision (AP, somma sui ranghi dove il richiamo cresce e interpretazione geometrica AUC-PR), Mean Average Precision (MAP) e principio di Macro-Averaging a tutela della coda lunga; varianti troncate per il Web e RecSys ($AP@K$ e $MAP@K$ con normalizzazione adattiva); Mean Reciprocal Rank (MRR) per ricerche puntuali (*known-item*, navigazionali, factoid).
  - Oltre la rilevanza binaria (rilevanza graduata multi-livello $0\text{--}3$): i due principi di Järvelin & Kekäläinen (utilità decrescente e decadimento posizionale dell'attenzione visiva); Cumulative Gain ($CG_p$) e cecità all'ordine; Discounted Cumulative Gain standard con sconto logaritmico $1/\log_2(i)$ e variante esponenziale industriale Google/Bing ($2^{r_i}-1$); Normalized Discounted Cumulative Gain (NDCG) con Ideal DCG ($IDCG$); tracciamento numerico completo a 10 documenti dalle slide didattiche ed esempio comparativo a 4 documenti sulla sensibilità alle inversioni di rango ($1.00$ vs. $0.9203$); quadro sinottico comparativo conclusivo.

- **Capitolo 2: Efficienza su Architetture CPU Moderne** (`02`)
  - Il ruolo dell'efficienza nell'IR: trade-off con l'efficacia, esperienza utente (latenze $< 50\text{--}100\text{ ms}$, time budget), scalabilità operativa (volume/capacità, repliche per fault tolerance) e sostenibilità ambientale dei data center.
  - Gerarchia di memoria e latenze (registri, L1I/L1D, L2, L3 LLC, DRAM, disco), regimi memory-bound vs. CPU-bound.
  - Principi di località spaziale e temporale (LRU), atomicità della cache line ($64\text{ byte}$) e hardware prefetching (stream, stride e fallimento sui pattern disordinati).
  - Caso di studio Rust su permutazione con singolo ciclo: scansione sequenziale `sum()` vs. pointer chasing `sum_by_jumping()`, rallentamenti da $13\times$ (L1) fino a $212\times$ (DRAM); risoluzione delle sfide didattiche (ammortamento su cache line e annullamento del rallentamento memory-bound).
  - Parallel computing: parallelismo a livello server (*embarrassingly parallel*) e nel singolo core (pipelining, superscalarità, SIMD).
  - Pipelining a 5 stadi (IF, ID, EX, MEM, WB), latenza, throughput, periodo $\tau$ e pipeline profonde ($15\text{--}20$ stadi).
  - Esecuzione superscalare ($IPC > 1$), execution ports parallele ed esperimento dell'*interleaving* (3-4 riduzioni indipendenti eseguite nello stesso tempo).
  - Pipeline hazards: strutturali (limiti del silicio), data hazards RAW (catene seriali con crollo del throughput e risoluzione con interleaving), control hazards (salti condizionati ed esecuzione speculativa).
  - Branch prediction: penalità di misprediction ($15\text{--}20$ cicli di clock sprecati per flush), esperimento empirico (dati casuali $3.5\text{ ns}$ vs. dati ordinati $1.2\text{ ns}$ vs. pattern alternato periodico $1.1\text{ ns}$) e tecniche branchless con predicati e istruzioni condizionali.
  - Vettorizzazione SIMD: registri vettoriali (SSE a 128 bit, AVX a 256 bit, AVX-512), auto-vettorizzazione vs. intrinsics; risoluzione dell'enigma iniziale con Compiler Explorer: auto-vettorizzazione di `sum()` con 4 somme a 64 bit simultanee (`vpaddq`) in L1 cache vs. impossibilità di vettorizzare `sum_by_jumping()`.
  - Quadro sinottico: mappatura dai vincoli micro-architetturali alle scelte ingegneristiche in Information Retrieval (indici compressi a blocchi, salti `nextGEQ`, decodifica SIMD-BP128).

- **Capitolo 3: Proprietà del Linguaggio Naturale e Preprocessing del Testo** (`03`)
  - Proprietà fondamentali del linguaggio naturale: migliaia di simboli e vocabolario aperto; legge di Zipf ($f \propto 1/r$, principio del minimo sforzo tra speaker e hearer, 313 parole che coprono oltre il 50% di Reuters-21578, leggi su significati $m \propto 1/\sqrt{f}$ e lunghezza dei termini).
  - Distribuzione lessicale: parole rare ed *hapax legomena* (trade-off tra riduzione della memoria e perdita di termini discriminanti); stopwords e ponderazione semantica (rischi del filtraggio cieco, frasi esatte e caso limite sentiment di MySQL).
  - Semantica composizionale vs. collocazioni (*make the bed*, *saltare la lezione*) ed espressioni idiomatiche (*break a leg*, *dalla padella nella brace*).
  - Sorgenti di ambiguità: morfologica/Part-of-Speech (*beat* sostantivo vs. verbo), semantica/polisemia (*interest* curiosità vs. tasso bancario) e sintattica (attaccamento preposizionale).
  - Conoscenza condivisa del mondo (*shared world knowledge*) e inferenze contestuali (*Lewis Hamilton*, *sisters vs. mothers*, *bike with helmet vs. electric engine*).
  - Dinamicità temporale, neologismi (*Tesla, googled, in the cloud, crowdfunded*) e formalizzazione di Natural Language Understanding (NLU) come problema AI-Complete.
  - Relazioni con altri tipi di dati: testo non strutturato vs. tabelle relazionali SQL, grafi (Link Graph, Knowledge Graph, PageRank, anchor text) e dati multimediali; concetto di *Processing Pipeline*.
  - Text processing in Python: download Web a basso livello con `urllib.request`; estrazione e pulizia DOM da HTML con `BeautifulSoup`; tokenizzazione e sentence splitting con `NLTK` (`word_tokenize`, `sent_tokenize` per la disambiguazione del punto fermo); esplorazione quantitativa con `FreqDist` e `Text`; rimozione stopwords.
  - Normalizzazione morfologica: Stemming euristico basato su regole (Algoritmo di Porter, `cars` $\to$ `car`, `was` $\to$ `wa`) vs. Lemmatizzazione morfosintattica profonda con dizionario (WordNet con tag POS, `was` $\to$ `be`).
  - Quadro sinottico della pipeline di preprocessing del testo in Python.

- **Capitolo 4: Rappresentazioni del Testo, Modello Booleano ed Evoluzione del Retrieval** (`04`)
  - Operazioni fondamentali sulle collezioni di testo: stemming, lemmatizzazione e rimozione delle stopword (trade-off di vocabolario).
  - Modelli di rappresentazione del testo ed esempi in Python:
    - Bag of Words (BoW): definizione, esempi in Python, vantaggi ed eliminazione della sintassi (*"I won, and thus you lose"* vs. *"I lose, and thus you won"* $\implies$ set identici).
    - Word N-grammi: preservazione del contesto e dell'ordine locale (*"united states"*), vantaggi e svantaggi (esplosione combinatoria $|\mathcal{V}|^n$).
    - Character N-grammi: scomposizione subword, tolleranza ai refusi di battitura (*rainbow* vs. *rainbaw*) e pro/contro.
  - Perché serve una rappresentazione documentale: verso il Vector Space Model e codifica binaria one-hot in $\mathbb{R}^{|\mathcal{F}|}$; estrema sparsità vettoriale ($> 99.9\%$).
  - Modello di retrieval booleano tradizionale: sintassi proposizionale (\texttt{AND}, \texttt{OR}, \texttt{NOT}), pro e contro, limiti strutturali e patologia del *Feast or Famine*.
  - Come estendere il modello booleano: transizione verso il Ranked Retrieval continuo e landscape storico della letteratura (era statistica, strutturale/PageRank, Machine Learning/LtR ed era neurale).
  - Quadro sinottico comparativo delle rappresentazioni testuali e modelli di retrieval.

- **Capitolo 5: Vector Space Model, Ponderazione TF-IDF e Similarità Coseno** (`05`)
  - Dall'estensione del booleano alla matrice di incidenza binaria termine-documento in $\{0, 1\}^{|\mathcal{V}| \times N}$.
  - Misure di similarità su insiemi: coefficiente di Jaccard, paradosso della lunghezza documentale (*"ides of march"*) e limiti strutturali (assenza di $tf$, assenza di $df$, penalizzazione dei testi lunghi).
  - Frequenza dei termini e rilevanza: matrice di conteggio dei termini, legge dei rendimenti marginali decrescenti e ponderazione sublineare logaritmica ($1 + \log_{10}(\text{tf})$).
  - Frequenza documentale ($df_t$) vs. Collection Frequency ($cf_t$): informatività semantica, rarit\`a e Inverse Document Frequency ($\text{idf}_t$).
  - Schema di ponderazione TF-IDF composito completo ed esercizio numerico svolto alla lavagna ($N=806\,791$, ribilanciamento raw vs. log-TF).
  - Documenti e query come vettori $N$-dimensionali nello Spazio Vettoriale (VSM) ed estrema sparsità vettoriale.
  - Come rispondere a una query nello spazio vettoriale: distanza euclidea ($L_2$), pro e contro, fallimento dimostrato sui documenti concatenati/duplicati ($d' = d \circ d$) e direzione vs. magnitudine.
  - Angolo tra vettori, prodotto scalare e Cosine Similarity; normalizzazione vettoriale della lunghezza $L_2$ sull'ipersfera unitaria.
  - Architettura computazionale disaccoppiata offline/online nei motori di ricerca in produzione.
  - Caso di studio comparativo completo su romanzi classici (Jane Austen vs. Emily Brontë).
  - Tassonomia standard della notazione SMART (`ddd.qqq`), protocollo asimmetrico `lnc.ltc` ed esercizio pratico guidato ($N=1\,000\,000$).
  - Diagramma di flusso concettuale integrato: pipeline NLP, VSM, ponderazione SMART e Cosine Similarity.

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
  - **Laboratorio pratico in Python su Dataset C4** (Lezione 12/10/2026): ingestione e tokenizzazione di porzione C4, classe `PostingList` con `nextGEQ` su `bisect_left`, algoritmi `taat_or`, `taat_and_nextGEQ`, `daat_and_linear`, `daat_and_nextGEQ`, `daat_or_heap` e benchmark sperimentale con speedup fino a oltre $200\times$ su query a selettività asimmetrica.
  - Applicazioni moderne nel retrieval neurale sparso (SPLADE), accelerazione hardware su GPU e vector search engine dedicati (Qdrant).
  - Tabella comparativa di sintesi finale: complessità computazionale, ingombro in RAM e capacità di skipping.

- **Capitolo 8: Elaborazione Efficiente di Query Top-$k$: WAND, MaxScore e Varianti a Blocchi** (`08`)
  - Architettura di retrieval a due stadi: collegamento con il candidate retrieval (BM25) e motivazione comportamentale dell'attenzione dell'utente sul web (primi 10-20 risultati, riformulazione se insoddisfatto).
  - Formulazione formale dell'Exact Top-$k$ Retrieval e gestione della coda con priorità tramite Min-Heap: ruolo della soglia dinamica $\tau$ come costo d'ingresso, costo $\mathcal{O}(n \log k)$, traccia numerica e simulazione esaustiva DAAT passo-passo con 4 termini (`rust`, `best`, `programming`, `language`) a confronto con l'Algoritmo 7.2.
  - Algoritmo WAND (*Weak AND*, Broder et al. 2003): definizione formale di Upper Bound di termine ($UB(t)$), costo di memoria $\mathcal{O}(|\mathcal{V}|)$, condizione di scarto sicuro, modello di costo hardware (*CPU reasoning vs pointer movements*), ordinamento dinamico per docID corrente e selezione del pivot document.
  - Tracciamento analitico dettagliato di WAND: determinazione del pivot a Doc 15, salto sicuro tramite `nextGEQ` e valutazione completa con innalzamento della soglia a $\tau = 3.7$.
  - Analisi critica e casi limite nel Dynamic Pruning: semantica disgiuntiva OR e termini assenti, inapplicabilità pratica a query AND, trade-off sui salti intermedi anticipati e dimostrazione algebrica dello scarto a priori di Doc 12.
  - Algoritmo MaxScore (Turtle & Flood 1995): partizionamento dinamico in liste essenziali e non-essenziali ($\sum UB < \tau$), ordinamento statico per $UB$ una sola volta, scansione DAAT selettiva sulle sole essenziali, stima ottimistica ed eliminazione del collo di bottiglia di riordinamento dinamico; traccia completa ed effetto della promozione dinamica delle liste.
  - Valutazione sperimentale su benchmark TREC 05 (collezione Gov2): confronto tra RankedOR, WAND, MaxScore, $\text{BMW}_{40}$ e $\text{VBMW}_{40}$; analisi della scalabilità e dell'overhead spaziale ($0.22\%$ vs $1.55\%$).
  - Limite degli Upper Bound globali e varianti a blocchi: Block-Max WAND (BMW, blocchi a dimensione fissa) e Variable Block-Max WAND (VBMW, blocchi a dimensione variabile adattati alla distribuzione dei punteggi con minimizzazione geometrica dell'area di sovrastima, fino a $50\times$ di accelerazione).
  - Sistemi reali e stato dell'arte industriale: l'ecosistema Apache Lucene / Elasticsearch, evoluzione a 4 stadi sintetizzata da Adrien Grand (2023) e divario decennale per la riscrittura dei codec di indice e la tolleranza a workload eterogenei.
  - Sintesi comparativa sinottica degli algoritmi Top-$k$.

- **Capitolo 9: Learning to Rank I: Fondamenti, Tassonomia e Framework Generale** (`09`)
  - Okapi BM25 fondazionale (Robertson & Zaragoza 2009, Manning et al.): genesi storica nel sistema Okapi alla City University di Londra, Probabilistic Relevance Framework (PRF) e log-odds di rilevanza.
  - Term Frequency Smoothing: limiti di Raw TF e Log-TF, funzione di saturazione asintotica $\tau(f_{t,d}) = \frac{(k_1+1)f_{t,d}}{k_1+f_{t,d}}$ verso il limite superiore finito $k_1+1$.
  - Pivoted Document Length Normalization: verbosità vs. ampiezza tematica, normalizzatore $B(d) = (1-b) + b \frac{|d|}{\text{avgdl}}$, perno a $\text{avgdl}$ e ruolo dell'iperparametro $b$.
  - Formula completa di Okapi BM25 con IDF probabilistica e best practices sugli iperparametri ($k_1 \in [1.2, 2.0]$, $b = 0.75$).
  - Decomposizione formale delle funzioni di ranking basata sulle rappresentazioni (Guo et al. 2020, Bruch et al. 2023: rappresentazione query $\phi$, documento $\psi$, interazione $\eta$, aggregatore $f$).
  - Oltre il modello Bag of Words (BoW): campi strutturati, testi di ancoraggio (*anchor text*), link graph e PageRank, segnali comportamentali (clic, dwell time) e proprietà della query.
  - Il paradigma del Machine Learning applicato al ranking: regressione vs. ranking posizionale, analogia del puzzle, disaccoppiamento tra Fase 1 (Training Offline) e Fase 2 (Inference Online) sotto Time Budget rigoroso.
  - Tassonomia delle feature in un motore di ricerca web (Bruch et al. 2023, Manning et al.): query-only, query-independent (statiche del documento) e query-dependent.
  - Pipeline di Two-Stage Retrieval: Base Ranker ad alto throughput su indice invertito ($N \approx 1\,000$) e Top Ranker LtR per la SERP ($k \approx 10\text{--}20$).
  - Esempio di classificazione per l'ad-hoc IR (Manning et al.): spazio bidimensionale $\langle \alpha, \omega \rangle$ (coseno vs. minima finestra di prossimità) e limiti della separazione lineare binaria.
  - Tassonomia canonica di Learning to Rank (Liu 2009):
    - *Pointwise*: predizione indipendente dello score del singolo documento (MSE, cross-entropy), cecità rispetto alla graduatoria.
    - *Pairwise*: preservazione delle preferenze di coppia ($d_i \succ d_j$), funzione di perdita logistica di RankNet (Burges et al. 2005) e calcolo dei gradienti per SGD; criticità strutturale dell'appiattimento delle coppie e divergenza con NDCG@$k$.
    - *Listwise*: ottimizzazione dell'intero elenco e teorema di non-derivabilità dell'operatore discreto di ordinamento ($\nabla_{\mathbf{\theta}} \text{sort} = \mathbf{0}$).
  - Quadro sinottico comparativo dei paradigmi di Learning to Rank.

- **Capitolo 10: Learning to Rank II: Pipeline Industriale, BM25F e Modelli ad Albero GBRT** (`10`)
  - Architettura operativa end-to-end di una pipeline LtR: ricezione query, espansione NLP, candidate retrieval su indice invertito, feature extraction/lookup densa ($D \approx 100\text{--}1\,000$), valutazione del modello supervisionato e vincolo del Time Budget ($\le 15\text{--}25\text{ ms}$ per inferenza, $< 20\,\mu\text{s}$ per candidato).
  - Apprendere un classificatore per la rilevanza di coppie query-documento nell'ad-hoc search: formulazione probabilistica, limiti strutturali (class imbalance severo, simmetria dell'errore, assenza di competizione locale).
  - Formulazione matematica precisa degli approcci di ranking (Bruch, Lucchese, Nardini 2023): spazio delle permutazioni $\mathfrak{S}_n$, formulazioni formali di Pointwise (MSE e cross-entropy), Pairwise (probabilità logistica sigmoide e perdita di RankNet con fattore $1/2$) e Listwise (ListNet con proiezione softmax sul simplesso delle probabilità e cross-entropia tra distribuzioni).
  - Estensione da BM25 a BM25F (*BM25 with Fields*, Robertson, Zaragoza, Taylor et al.): combinazione convessa delle frequenze normalizzate di campo prima della saturazione asintotica, formule complete e parametri per campo ($w_s, b_s, k_1$).
  - Analisi critica di BM25F: vantaggi (saturazione asintotica corretta, ponderazione zone, controllo lunghezza $b_s$) e svantaggi (esplosione dello spazio a $2S+1$ parametri liberi, interdipendenza non lineare, overhead computazionale).
  - Inquadramento dell'ottimizzazione di BM25F in un problema di Learning to Rank: spazio delle ipotesi, training set e massimizzazione di NDCG@10; pro e contro dell'approccio LTR su BM25F.
  - Calibrazione dei parametri: confronto analitico tra Grid Search ($\mathcal{O}(G^{2S+1})$, impraticabile per $S \ge 4$) e Discesa di Gradiente; superamento della non-derivabilità di NDCG tramite funzione di perdita surrogata pairwise differenziabile (RankNet).
  - Problemi fondamentali dell'apprendimento del ranking: natura discreta a gradino delle metriche (MAP, NDCG), non convessità e non derivabilità dell'operatore di ordinamento ($\nabla_{\mathbf{s}} \text{sort}(\mathbf{s}) = \mathbf{0}$ quasi ovunque), intrattabilità teorica e NP-difficoltà dell'ottimizzazione diretta.
  - Modelli ad albero per il ranking: anatomia di un Regression Tree, partizione dello spazio $\mathbb{R}^D$ in $J$ regioni ortogonali disgiunte, algoritmo di Recursive Binary Splitting con criterio di minimizzazione della varianza residua (MSE), calcolo analitico del valore costante predetto alle foglie come media empirica ed esempio numerico passo-passo.
  - Gradient Boosted Regression Trees (GBRT / MART, Friedman 2001): espansione additiva $F_M(\mathbf{x}) = F_0(\mathbf{x}) + \sum \eta h_m(\mathbf{x})$, discesa di gradiente funzionale nello spazio delle funzioni, calcolo degli pseudo-residui come gradiente negativo della perdita e shrinkage $\eta$.
  - Motivazioni della supremazia di GBRT su dati tabulari in IR: invarianza monotona di scala, isolamento degli outlier, cattura spontanea delle interazioni non lineari tra feature e gestione nativa dei valori mancanti.
  - Da GBRT a LambdaMART (Burges 2010): addestramento di regression tree su pseudo-gradienti virtuali $\lambda$ pesati sulla variazione marginale $|\Delta \text{NDCG}|$. Librerie industriali ad alte prestazioni (LightGBM con istogrammi a 8 bit e CatBoost con alberi simmetrici branchless).
  - Quadro sinottico comparativo: Okapi BM25, BM25F, Classificatore Lineare, Regression Tree singolo, GBRT/MART e LambdaMART.
  - Problemi fondamentali dell'apprendimento del ranking: natura discreta a gradino delle metriche (MAP, NDCG), non convessità e non derivabilità dell'operatore di ordinamento ($\nabla_{\mathbf{s}} \text{sort}(\mathbf{s}) = \mathbf{0}$ quasi ovunque), intrattabilità teorica e NP-difficoltà dell'ottimizzazione diretta.
  - Modelli ad albero per il ranking: anatomia di un Regression Tree, partizione dello spazio $\mathbb{R}^D$ in $J$ regioni ortogonali disgiunte, algoritmo di Recursive Binary Splitting con criterio di minimizzazione della varianza residua (MSE), calcolo analitico del valore costante predetto alle foglie come media empirica ed esempio numerico passo-passo.
  - Gradient Boosted Regression Trees (GBRT / MART, Friedman 2001): espansione additiva $F_M(\mathbf{x}) = F_0(\mathbf{x}) + \sum \eta h_m(\mathbf{x})$, discesa di gradiente funzionale nello spazio delle funzioni, calcolo degli pseudo-residui come gradiente negativo della perdita e shrinkage $\eta$.
  - Motivazioni della supremazia di GBRT su dati tabulari in IR: invarianza monotona di scala, isolamento degli outlier, cattura spontanea delle interazioni non lineari tra feature e gestione nativa dei valori mancanti.
  - Da GBRT a LambdaMART (Burges 2010): addestramento di regression tree su pseudo-gradienti virtuali $\lambda$ pesati sulla variazione marginale $|\Delta \text{NDCG}|$. Librerie industriali ad alte prestazioni (LightGBM con istogrammi a 8 bit e CatBoost con alberi simmetrici branchless).
  - Quadro sinottico comparativo: Okapi BM25, BM25F, Classificatore Lineare, Regression Tree singolo, GBRT/MART e LambdaMART.

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
