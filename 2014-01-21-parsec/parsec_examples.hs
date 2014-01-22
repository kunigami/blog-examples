import Text.Parsec
-- Do not include the whole library because it will cause name conflicts with Text.Parsec
import Control.Applicative ((<$), (<*), (*>), (<$>), (<*>))
import Data.Char

-- Helper function to avoid boiler plate
test p = parse p ""

--------------------------------------------------------------------------------
-- Sample toy parsers
--------------------------------------------------------------------------------
charAParser:: Parsec String st Char
charAParser = (char 'a')

wordParser:: Parsec String st String
wordParser = many $ noneOf [' ']

secondWordParser:: Parsec String st String
secondWordParser = wordParser *> (char ' ')  *> wordParser

parseTwoWords:: String -> Either ParseError [String]
parseTwoWords = parse twoWordsParser ""

parseWords:: String -> Either ParseError [String]
parseWords = parse wordsParser ""

twoWordsParser:: Parsec String st [String]
twoWordsParser = listfy <$> wordParser <*> ((char ' ') *> wordParser)
                   where listfy a b = [a, b]

wordsParser:: Parsec String st [String]
wordsParser = (:) <$> wordParser <*> many ((char ' ') *> wordParser)

dogCatParser:: Parsec String st String
dogCatParser = (string "cat") <|> (string "dog")

camelCatParser:: Parsec String st String
camelCatParser = try (string "camel") <|> (string "cat")

csvParser:: Parsec String st [[String]]
csvParser = lineParser `endBy` newline <* eof
              where lineParser = cellParser `sepBy` (char ',')
                    cellParser = many $ noneOf ",\n"

--------------------------------------------------------------------------------
-- Expression parser
--------------------------------------------------------------------------------
type TNumber = Int

data TOperator = TAdd
               | TSubtract
                 deriving (Eq, Ord, Show)

data TExpression = TNode (TExpression) TOperator (TExpression)
                 | TTerminal TNumber
                   deriving (Show)

numberParser:: Parsec String st TNumber
numberParser = read <$> (many $ oneOf "0123456789")

operatorParser:: Parsec String st TOperator
operatorParser = chooseOp <$> (oneOf "+-")
                   where chooseOp '+' = TAdd
                         chooseOp '-' = TSubtract

expressionParser:: Parsec String st TExpression
expressionParser = (between (char '(') (char ')') binaryExpressionParser) <|>
                   (TTerminal <$> numberParser)

binaryExpressionParser:: Parsec String st TExpression
binaryExpressionParser = TNode <$> expressionParser <*> operatorParser <*> expressionParser

evaluate:: TExpression -> TNumber
evaluate (TNode exp1 TAdd exp2)      = (evaluate exp1) + (evaluate exp2)
evaluate (TNode exp1 TSubtract exp2) = (evaluate exp1) - (evaluate exp2)
evaluate (TTerminal v)     = v
