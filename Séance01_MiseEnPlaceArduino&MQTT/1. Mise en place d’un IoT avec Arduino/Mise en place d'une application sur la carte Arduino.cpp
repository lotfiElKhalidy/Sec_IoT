// Code pour faire clignoter une LED : BLINK
void setup() 
{
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() 
{
    static bool state = false;

    digitalWrite(LED_BUILTIN, state);
    state = !state;
    delay(100);     // 0,1s
}

/*___________________ Exercice : Allumer les DELs à l'aide des boutons-poussoirs __________________
    Compléter le code suivant pour qu’en appuyant sur le bouton 3 la DEL D5 s'allume 
    pendant 3 secondes et puis s'éteint et la même chose pour le couple bouton 2 et la DEL
    D6.
*/

// définition des différentes connexions
// GPIO General Purpose Input/Output

// Les LEDs
const int led_D5 = 13;
const int led_D6 = 12;

// Les boutons-poussoir
const int bouton_S2 = 8;
const int bouton_S3 = 9;

// Les états
int etat_S2, etat_S3;

// fonction d'initialisation de la carte
void setup()
{
    // initialisation des broches 12 et 13 comme étant des sorties
    pinMode(led_D5, OUTPUT);
    pinMode(led_D6, OUTPUT);

    // initialisation des broches 8 et 9 comme étant des entrées
    pinMode(bouton_S2, INPUT);
    pinMode(bouton_S3, INPUT); 
}

// fonction principale, elle se répète (s’exécute) à l'infini
void loop()
{
    // On lit l'état des broches 8 et 9 
    etat_S2 = digitalRead(bouton_S2);
    etat_S3 = digitalRead(bouton_S3);

    // Si le bouton 2 est appuyé, on allume la LED 6 pour 3 secondes
    if (etat_S2 == LOW)
    {
        // Pour changer l'état de la broche 12 (on allume la LED)
        digitalWrite(led_D6, HIGH);
        // 3000 means 3s
        delay(3000);
        // (On éteint la LED)
        digitalWrite(led_D6, LOW);
    }

    if (etat_S3 == LOW)
    {
        digitalWrite(led_D5, HIGH);
        delay(3000);
        digitalWrite(led_D5, LOW); 
    }
}

/* _____________________________________ Gestion des interruptions ____________________________________
    En informatique, une interruption est une suspension temporaire de l'exécution d'un programme 
    informatique par le microcontrôleur afin d'exécuter un programme prioritaire (appelé service 
    d'interruption). Les interruptions sont provoquées par exemple par des changements d’état 
    d’une entrée numérique.
*/

// définition des différentes connexions
// GPIO General Purpose Input/Output
const int led_D5 = 13;
const int led_D6 = 12;

const int bouton_S2 = 8;

const int interrupt_bouton_S3 = 9;

int etat_S2, etat_S3;

// fonction d'initialisation de la carte
void setup()
{
    // initialisation des broches 12 et 13 comme étant des sorties
    pinMode(led_D5, OUTPUT);
    pinMode(led_D6, OUTPUT);

    // initialisation des broches 8 et 9 comme étant des entrées
    pinMode(bouton_S2, INPUT);
    pinMode(interrupt_bouton_S3, INPUT);

    // la broche 9 va générer une interruption lorsqu'elle sera à l'état BAS
    attachInterrupt(digitalPinToInterrupt(interrupt_bouton_S3), reagir_S3_Bas, LOW); 
}

// fonction principale, elle se répète (s’exécute) à l'infini
void loop()
{
    etat_S2 = digitalRead(bouton_S2);

    if(etat_S2 == LOW)
    {
        digitalWrite(led_D6, HIGH);
        delay(3000);
        digitalWrite(led_D6, LOW);
    }
}

void reagir_S3_Bas() 
{
    digitalWrite(led_D5, HIGH);
    delay(3000);
    digitalWrite(led_D5, LOW);
}