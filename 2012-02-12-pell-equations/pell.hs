-- Encontra as k primeiras solucoes da equacao de pell
pell_solutions n k = find_solutions k f0 g0 f0 g0 sqn
                      where sqn = sqrt $ fromIntegral n
                            f = fundamental_solution n sqn
                            p = fromIntegral $ fst f
                            q = fromIntegral $ snd f
                            f0 = p + q*sqn
                            g0 = p - q*sqn


-- Procura um par representando a solucao fundamental 
fundamental_solution n sqn = find_solution n sqn a 1 a 0 1
                          where a = truncate sqn

-- Procura a solucao fundamental recursivamente
find_solution n r a p0 p1 q0 q1
                                | p1*p1 - n*q1*q1 == 1 = (p1, q1)
                                | otherwise            = find_solution n r' a' p1 (a'*p1 + p0) q1 (a'*q1 + q0)
                                  where r' = 1.0/(r - (fromIntegral a))
                                        a' = truncate r'

-- Encontra as k-1 primeiras solucoes da equacao de pell,dada a solucao fundamental
-- Nota: pre-computa alguns valores para maior eficiencia
find_solutions k fk gk f0 g0 sqn
                              | k == 0 = [ ]
                              | otherwise = (p,q) : (find_solutions (k-1) (fk*f0) (gk*g0) f0 g0 sqn)
                                where p = truncate $ (fk + gk)/2 + 0.0001
                                      q = truncate $ (fk - gk)/(2*sqn) + 0.0001
              