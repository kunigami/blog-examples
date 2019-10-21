import Control.Comonad

data Universe x = Universe [x] x [x]

goRight (Universe a b (c:cs)) = Universe (b:a) c cs
goLeft  (Universe (a:as) b c) = Universe as a (b:c)

instance Functor Universe where
    fmap f (Universe a b c) = Universe (map f a) (f b) (map f c)

instance Comonad Universe where 
    -- coreturn
    extract (Universe _ b _) = b
    -- cojoin
    duplicate a = Universe (tail $ iterate goLeft a) a (tail $ iterate goRight a)

rule :: Universe Bool -> Bool
rule (Universe (l:_) x (r:_)) = not (l && x && not r || (l == x))

-- Move i positions to the right or i position to the left (if i is negative)
shift :: Int -> Universe a -> Universe a
shift n u = (iterate (if n < 0 then goLeft else goRight) u) !! abs n

-- Return the array [-len, len] surrounding x
sample :: Int -> Universe a -> [a]
sample len u = take (2*len) $ half $ shift (-len) u 
       where half (Universe _ x ls) = [x] ++ ls

boolsToString :: [Bool] -> String
boolsToString = map (\x -> if x then '#' else ' ') 

toString :: Universe Bool -> String
toString = boolsToString  . sample 50

test = putStr . unlines . (take 20) . (map toString) $ iterate (=>> rule) example
        where example = (Universe (repeat False) True (repeat False))
