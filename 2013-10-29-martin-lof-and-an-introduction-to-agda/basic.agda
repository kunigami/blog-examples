--------------------------------------------
-- Simple examples exploring Agda syntax  --
--------------------------------------------
module basic where

-- Booleans
data Bool : Set where
  true : Bool
  false : Bool

not : Bool -> Bool
not true = false
not false = true

-- Natural numbers
data Nat : Set where
  zero : Nat
  suc  : Nat -> Nat

-- addition
_+_ : Nat -> Nat -> Nat 
zero  + m = m
suc n + m = suc (n + m)

-- multiplication
_*_ : Nat -> Nat -> Nat
zero  * m = zero
suc n * m = m + n * m

-- define priority
infixl 6 _*_
infixl 4 _+_

-- definition of a list with parametrized type
data List (A : Set) : Set where
  -- empty operator
  [] : List A
  -- append operator
  _::_ : A -> List A -> List A


-- parametrized types in functions
identity : (A : Set) -> A -> A
identity A x = x

-- example of usage
zero' : Nat
zero' = identity Nat zero

-- need to provide the type when calling identity

-- Complex example
-- A is of type Set
-- B is a function from A to Set
-- Param 1: function f which takes x of type a and apply B to it
-- Param 2: eleement a of type A
-- Return : function applied to element a
apply : (A : Set) (B : A -> Set) ->
  ((x : A) -> B x) -> (a : A) -> B a
apply A B f a = f a

-- implicity type (type inference)
-- omitting parameter in definition and call
id : {A : Set} -> A -> A
id x = x

true' : Bool
true' = id true

mape : (A B : Set) -> (A -> B) -> List A -> List B 
mape A B f [] = []
mape A B f (x :: xs) = f x :: mape A B f xs

-- implicit call -- you tell exactly which argument you're providing
map : {A B : Set} -> (A -> B) -> List A -> List B 
map f [] = []
map f (x :: xs) = f x :: map f xs

-- Concatenation
_++_ : {A : Set} -> List A -> List A -> List A
[]        ++ ys = ys
(x :: xs) ++ ys = x :: (xs ++ ys)

-- Families of types
data Vec (A : Set) : Nat -> Set where
  []   : Vec A zero
  -- length is infered
  _::_ : {n : Nat} -> A -> Vec A n -> Vec A (suc n)
--  conc : (n : Nat) -> A -> Vec A n -> Vec A (suc n)
  
-- data type has two parameters, Nat and Set. Nat is the type of the
-- index and Set the type of the value

-- Doesn't need to check for empty lists. Restriction is encoded in
-- the function type!
head : {A : Set}{n : Nat} -> Vec A (suc n) -> A
head (x :: xs) = x 

-- vector map
vmap : {A B : Set}{n : Nat} -> (A -> B) -> Vec A n -> Vec B n
vmap f []        = []
vmap f (x :: xs) = f x :: vmap f xs

------------------------
-- Programs as proofs --
------------------------

data False : Set where
data True  : Set where

isTrue : Bool -> Set
isTrue true = True
isTrue false = False

-- Definition of the < operator
_<_ : Nat -> Nat -> Bool
_ < zero = false
zero  < suc n = true
suc m < suc n = m < n

-- Definition of the length operator
length : {A : Set} -> List A -> Nat
length [] = zero
length (x :: xs) = suc (length xs)

-- Function that looks up the i-th element in a list
-- param 1: list
-- param 2: look up index
-- param 3: proof
lookup : {A : Set}(xs : List A)(n : Nat) -> isTrue (n < length xs) -> A
lookup [] n ()
lookup (x :: xs) zero p = x
lookup (x :: xs) (suc n) p = lookup xs n p

-- Data type that can take two parameters
data _==_ {A : Set}(x : A) : A -> Set where
  refl : x == x

-- Instead of function we define as a new type
data _<=_ : Nat -> Nat -> Set where
  leq-zero : {n : Nat} -> zero <= n
  leq-suc  : {m n : Nat} -> m <= n -> suc m <= suc n

-- Function leq transitive. Given the relation of the pairs (l, m) and
-- (m, n), infers the relation between (l, n)
leq-trans : {l m n : Nat} -> l <= m -> m <= n -> l <= n
-- l <= m = 0, so l <= 0
leq-trans leq-zero _ = leq-zero
leq-trans (leq-suc p) (leq-suc q) = leq-suc (leq-trans p q)
