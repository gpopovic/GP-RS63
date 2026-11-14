@echo off
CHARSET UTF8
TITLE Erstellung des Company_OS Ordnerstruktur-System...
COLOR 0A

SET "BASE_DIR=C:\Projects\Triton_AI_Corp"

echo ============================================================
echo   Erstelle vollstaendiges Unternehmens-OS unter:
echo   %BASE_DIR%
echo ============================================================
echo.

:: 1. Governance & Strategy
mkdir "%BASE_DIR%\01_Governance_and_Strategy\EOS_OKRs"
mkdir "%BASE_DIR%\01_Governance_and_Strategy\Legal_Templates"
mkdir "%BASE_DIR%\01_Governance_and_Strategy\Finance_and_Pricing"

:: 2. Organization & Roles
mkdir "%BASE_DIR%\02_Organization_and_Roles\Roles_Descriptions"
mkdir "%BASE_DIR%\02_Organization_and_Roles\Internal_Coaches"
mkdir "%BASE_DIR%\02_Organization_and_Roles\Workflows_and_SOPs\Software_Engineering"
mkdir "%BASE_DIR%\02_Organization_and_Roles\Workflows_and_SOPs\Civil_and_Structural"
mkdir "%BASE_DIR%\02_Organization_and_Roles\Workflows_and_SOPs\Design_and_UX"

:: 3. Knowledge Base & RAG
mkdir "%BASE_DIR%\03_Knowledge_Base_RAG\Standards_and_Norms"
mkdir "%BASE_DIR%\03_Knowledge_Base_RAG\Code_Snippets_and_Templates"
mkdir "%BASE_DIR%\03_Knowledge_Base_RAG\Statics_and_Physics_Formulas"

:: 4. Execution Engine
mkdir "%BASE_DIR%\04_Execution_Engine\LangGraph_Pipelines"
mkdir "%BASE_DIR%\04_Execution_Engine\Prompts_and_SystemInstructions"
mkdir "%BASE_DIR%\04_Execution_Engine\Automatic_Validators"
mkdir "%BASE_DIR%\04_Execution_Engine\Docker_Environments"

:: 5. Human Interface & Ops
mkdir "%BASE_DIR%\05_Human_Interface_and_Ops\Task_Boards"
mkdir "%BASE_DIR%\05_Human_Interface_and_Ops\Manual_Quality_Gates"

:: 6. Projects & Clients
mkdir "%BASE_DIR%\06_Projects_and_Clients\Internal_R_and_D"
mkdir "%BASE_DIR%\06_Projects_and_Clients\External_Clients"

echo Ordnerstruktur erfolgreich erstellt!
echo.
echo Erstelle Platzhalter-Dateien fuer das Personal Trio...

:: Generiere Platzhalter fuer den Korrektur-Coach
(
echo # ROLE: DER KORREKTOR ^(Devil's Advocate / Analytiker^)
echo.
echo ## Ziel
echo Findet kritische Denkfehler, unvollstaendige Spezifikationen, Sicherheitsluecken oder Normenverstoesse ^(ASPICE, ISO, DIN^).
echo.
echo ## Sprachen
echo Deutsch, English, Srpski.
echo.
echo ## Verhalten
echo - Bestaetigt Entwuerfe nicht blind.
echo - Sucht zu 90%% nach Lücken und Risiken.
) > "%BASE_DIR%\02_Organization_and_Roles\Internal_Coaches\ROLE_Korrektor.md"

:: Generiere Platzhalter fuer den Trainer-Coach
(
echo # ROLE: DER TRAINER ^(Skill-Booster ^& Mentor^)
echo.
echo ## Ziel
echo Stellt sicher, dass das tiefe Verstaendnis hinter Entscheidungen und Code erhalten bleibt und ausgebaut wird.
echo.
echo ## Sprachen
echo Deutsch, English, Srpski.
echo.
echo ## Verhalten
echo - Stellt gezielte Transferfragen.
echo - Erklaert Konzepte tiefgruendig und praegnant.
) > "%BASE_DIR%\02_Organization_and_Roles\Internal_Coaches\ROLE_Trainer.md"

:: Generiere Platzhalter fuer den Improver-Coach
(
echo # ROLE: DER IMPROVER ^(Senior Architect / Refactoring Boss^)
echo.
echo ## Ziel
echo Hebt funktionierenden 80%%-Code oder Entwuerfe auf Senior-Niveau ^(Clean Code, Performance, Elegance^).
echo.
echo ## Sprachen
echo Deutsch, English, Srpski.
echo.
echo ## Verhalten
echo - Zeigt konkretes Refactoring.
echo - Erklaert die Vorteile bezueglich Skalierbarkeit und Wartungsarmut.
) > "%BASE_DIR%\02_Organization_and_Roles\Internal_Coaches\ROLE_Improver.md"

echo.
echo ============================================================
echo   FERTIG! Dein Unternehmens-OS ist bereit unter:
echo   %BASE_DIR%
echo ============================================================
pause