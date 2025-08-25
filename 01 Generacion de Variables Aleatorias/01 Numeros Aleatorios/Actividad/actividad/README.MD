
% jupyter nbconvert /notebook.ipynb --to latex


    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    


    \usepackage{newunicodechar}
    \newunicodechar{∼}{\ensuremath{\sim}}
    \newunicodechar{←}{\ensuremath{\leftarrow}}
    \newunicodechar{…}{\ldots}


    % --- header con título de subsección + número de sección ---
    \usepackage{etoolbox}
    \setcounter{secnumdepth}{0}
    % centrar el header
    \pretocmd{\section}{\clearpage}{}{}
    % \pretocmd{\subsection}{\clearpage}{}{}

    \renewcommand{\contentsname}{Tabla de Contenidos}
    % o, si ya cargaste hyperref:
    \hypersetup{hidelinks}

    %\usepackage{newtxmath, newtxtext}

    \begin{document}
        
        

    % --- Portada académica ---
    \begin{titlepage}
    \newgeometry{top=5cm,bottom=3.0cm,left=3.0cm,right=3.0cm}
    \centering

            \LARGE{\textbf{Actividad 1: Simulación
    Estocástica}}\\[0.5cm]

    \small
    \textbf{Curso:} Temas Selectos I: O25 LAT4032 1\\

    \textbf{Profesor:} Rubén Blancas Rivera\\

    \textbf{Alumnos:} auau 1, auau 2, auau 3\\  

    \textbf{Universidad:} Universidad de las Américas Puebla\\

    \textbf{Fecha:} 2025-08-15
        
    \restoregeometry
    \end{titlepage}
    % --- Fin portada ---
    \newpage
    \tableofcontents



    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
    %
