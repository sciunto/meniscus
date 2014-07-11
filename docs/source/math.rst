Math
====

Problem
-------

The Laplace law is:

.. math::

   \gamma \left( - \frac{r''}{(1+r'^2)^{3/2}} + \frac{1}{r(1+r'^2)^{1/2}}  \right) = - \rho g z

for an interface :math:`r(z)`, where :math:`z` is the vertical coordinate and :math:`r` the distance to the center of the cylinder (or pin).


Each length is made dimensionless by the capillary length:

.. math::

    \kappa^{-1} = \sqrt{\gamma/(\rho g)}

Thus, we have to solve:

.. math::

    \tilde{r}'' = \tilde{z} (1+\tilde{r}'^2)^{3/2}  + (1+\tilde{r}'^2) / \tilde{r}

To do so, we rewrite this 2nd order equation to two first order ODE:

.. math::

    \frac{d\tilde{r}}{d\tilde{z}} = R

    \frac{dR}{d\tilde{z}} = \tilde{z} (1+R^2)^{3/2} + \frac{1+R^2 }{\tilde{r}}


Analytic cases
--------------
