

Resultado. Bajo la transformación polar
\[
(r,\theta)=T(x,y)=\Big(\sqrt{x^2+y^2},\ \operatorname{atan2}(y,x)\Big),\quad r>0,\ \theta\in(0,2\pi],
\]
con inversa \(T^{-1}(r,\theta)=(x,y)=(r\cos\theta,r\sin\theta)\), la densidad conjunta de \((R,\Theta)=T(X,Y)\) es
\[
f_{R,\Theta}(r,\theta)=\frac{r}{2\pi}\,e^{-r^{2}/2},\qquad (r,\theta)\in(0,\infty)\times(0,2\pi].
\]

Demostración, paso a paso.

1) Datos de partida.  
Se da \((X,Y)\) con densidad
\[
f_{X,Y}(x,y)=\frac{1}{2\pi}\exp\!\left(-\frac{1}{2}(x^{2}+y^{2})\right),\quad (x,y)\in\mathbb{R}^{2}.
\]
La recta \(\{x=0\}\) tiene probabilidad cero bajo una densidad continua, así que la definición \(\theta=\tan^{-1}(y/x)\) se interpreta rigurosamente como \(\theta=\operatorname{atan2}(y,x)\) y no afecta el resultado “casi seguro”.

2) Transformación e inversa.  
Defina
\[
R=\sqrt{X^{2}+Y^{2}},\qquad \Theta=\operatorname{atan2}(Y,X)\in(0,2\pi].
\]
La inversa es
\[
X=R\cos\Theta,\qquad Y=R\sin\Theta,
\]
con dominio \(\mathcal{D}=\{(r,\theta):r>0,\ \theta\in(0,2\pi]\}\).

3) Jacobiano del cambio de variables.  
Construya la matriz jacobiana de \(T^{-1}:(r,\theta)\mapsto(x,y)\):
\[
J(r,\theta)=
\begin{pmatrix}
\partial x/\partial r & \partial x/\partial \theta\\[2pt]
\partial y/\partial r & \partial y/\partial \theta
\end{pmatrix}
=
\begin{pmatrix}
\cos\theta & -r\sin\theta\\
\sin\theta & \ \ r\cos\theta
\end{pmatrix}.
\]
Su determinante es
\[
\det J(r,\theta)=r\big(\cos^{2}\theta+\sin^{2}\theta\big)=r.
\]
Por tanto, el factor jacobiano absoluto es \(|\det J(r,\theta)|=r\).

4) Fórmula de cambio de variables.  
Para \((r,\theta)\in\mathcal{D}\),
\[
f_{R,\Theta}(r,\theta)
=
f_{X,Y}\big(x,y\big)\,\big|\det J(r,\theta)\big|
\ \ \text{evaluando en}\ \ (x,y)=(r\cos\theta,r\sin\theta).
\]
Sustituyendo,
\[
x^{2}+y^{2}=(r\cos\theta)^{2}+(r\sin\theta)^{2}=r^{2},
\]
de modo que
\[
f_{X,Y}(r\cos\theta,r\sin\theta)=\frac{1}{2\pi}\exp\!\left(-\frac{1}{2}r^{2}\right).
\]
Multiplicando por el jacobiano:
\[
f_{R,\Theta}(r,\theta)=\frac{1}{2\pi}\exp\!\left(-\frac{1}{2}r^{2}\right)\cdot r
=\frac{r}{2\pi}\exp\!\left(-\frac{r^{2}}{2}\right).
\]

5) Verificación de normalización.  
Integre sobre \(\mathcal{D}\):
\[
\int_{0}^{2\pi}\!\!\int_{0}^{\infty}\frac{r}{2\pi}e^{-r^{2}/2}\,dr\,d\theta
=\left(\int_{0}^{2\pi}\frac{d\theta}{2\pi}\right)\left(\int_{0}^{\infty} r e^{-r^{2}/2}\,dr\right).
\]
Para la integral radial use la sustitución \(u=\tfrac{1}{2}r^{2}\Rightarrow du=r\,dr\):
\[
\int_{0}^{\infty} r e^{-r^{2}/2}\,dr=\int_{0}^{\infty} e^{-u}\,du=1.
\]
La integral angular vale \(1\). Producto \(1\cdot 1=1\). Es una densidad válida.

6) Consecuencias inmediatas.  
Factorización:
\[
f_{R,\Theta}(r,\theta)=\underbrace{\left(\frac{1}{2\pi}\right)}_{f_{\Theta}(\theta)}\ \underbrace{\left(r e^{-r^{2}/2}\right)}_{f_{R}(r)},\quad r>0,\ \theta\in(0,2\pi],
\]
por lo que \(R\) y \(\Theta\) son independientes,
\[
\Theta\sim \mathrm{Unif}(0,2\pi],\qquad R\sim\text{Rayleigh}(\sigma=1),
\]
con densidad \(f_{R}(r)=r e^{-r^{2}/2}\) para \(r>0\).

7) Conexión con Box–Muller.  
Si \(U_{1},U_{2}\sim\mathrm{Unif}(0,1)\) independientes y se define
\[
R=\sqrt{-2\ln U_{1}},\qquad \Theta=2\pi U_{2},
\]
entonces \(R\) tiene la densidad \(r e^{-r^{2}/2}\) y \(\Theta\) es uniforme e independiente. Por la inversa polar,
\[
X=R\cos\Theta,\qquad Y=R\sin\Theta
\]
tienen precisamente la densidad conjunta inicial, i.e., \(X,Y\) son normales estándar independientes. Esto completa el fundamento del método. \(\square\)