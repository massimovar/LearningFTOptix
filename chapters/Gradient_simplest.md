# Gradient: Simplest Way

## One sentence
A gradient is the slope: how much the loss changes when one parameter changes a little.

## Practical formula
For a parameter w:

gradient = d(loss) / dw

If exact derivative is hard, use a tiny-number estimate:

gradient ~= (loss(w + e) - loss(w)) / e

where e is very small (for example 0.0001).

## 3-step recipe
1. Compute current loss with current w.
2. Increase w by a tiny e, compute new loss.
3. Divide loss change by e.

That number is the gradient.

## Tiny numeric example
Let:

loss(w) = (w - 3)^2

At w = 5:

1. loss(5) = (5 - 3)^2 = 4
2. choose e = 0.001
3. loss(5.001) = (2.001)^2 = 4.004001
4. gradient ~= (4.004001 - 4) / 0.001 = 4.001

So gradient is about 4 (exact derivative is 2*(w-3)=4 at w=5).

## Why we care
Update rule in gradient descent:

w_new = w_old - lr * gradient

- If gradient is positive, w goes down.
- If gradient is negative, w goes up.

This moves w in the direction that reduces loss.

## Backprop in one line
Backprop is just a fast way to compute these gradients for all weights in all layers.
