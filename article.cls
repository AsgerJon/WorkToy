\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{coverletter}[2023/05/26 Cover Letter Class]

% Margins
\usepackage[top=2.5cm, bottom=2.5cm, left=2.5cm, right=2.5cm]{geometry}

% Title formatting
\renewcommand{\maketitle}{
    \begin{center}
    {\Large\textbf{\@title}}
        \par
    \end{center}
}

% Author formatting
\renewcommand{\author}[1]{
    \begin{center}
        \textbf{#1}\par
    \end{center}
}

% Date formatting
\renewcommand{\date}[1]{}

\endinput
