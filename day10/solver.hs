import Data.List
import Data.Maybe
import qualified Data.Map as Map
import Utils

getInput :: IO String
getInput = do
    contents <- readFile "input.txt"
    return contents


type Parsed = [Result]
type Sol1 = Int
type Sol2 = Int


data Result = Ok | Corrupted Char | Incomplete [Char] deriving Show
isCorrupted (Corrupted _) = True
isCorrupted _ = False
isIncomplete (Incomplete _) = True
isIncomplete _ = False


brackets = Map.fromList [('(', ')'), ('[', ']'), ('{', '}'), ('<', '>')]
matching c = fromJust $ Map.lookup c brackets

syntaxCheck :: String -> Result
syntaxCheck = syntaxCheck' []

syntaxCheck' :: [Char] -> String -> Result
syntaxCheck' [] "" = Ok
syntaxCheck' stack "" = Incomplete (reverse stack)
syntaxCheck' [] (c:rest)
    | elem c "([{<" = syntaxCheck' [c] rest
    | otherwise = Corrupted c
syntaxCheck' (s:stack) (c:rest)
    | elem c "([{<" = syntaxCheck' (c:s:stack) rest
    | elem c ")]}>" = if c == matching s then
                                         syntaxCheck' stack rest
                                         else
                                         Corrupted c


parse :: String -> Parsed
parse =  map syntaxCheck . lines 


corruptedScore (Corrupted ')') = 3
corruptedScore (Corrupted ']') = 57
corruptedScore (Corrupted '}') = 1197
corruptedScore (Corrupted '>') = 25137

incompleteScore (Incomplete []) = 0
incompleteScore (Incomplete (c:cs))
    | c == '(' = incompleteScore (Incomplete cs) * 5 + 1
    | c == '[' = incompleteScore (Incomplete cs) * 5 + 2
    | c == '{' = incompleteScore (Incomplete cs) * 5 + 3
    | c == '<' = incompleteScore (Incomplete cs) * 5 + 4

solve1 :: Parsed -> Sol1
solve1 = sum . map corruptedScore . filter isCorrupted


solve2 :: Parsed -> Sol2
solve2 parsed = (!! (length incompletes `div` 2)) . sort . map incompleteScore $ incompletes
        where
                incompletes = filter isIncomplete parsed


testdata = "[({(<(())[]>[[{[]{<()<>>\n\
\[(()[<>])]({[<{<<[]>>(\n\
\{([(<{}[<>[]}>{[]{[(<()>\n\
\(((({<>}<{<{<>}{[]{[]{}\n\
\[[<[([]))<([[{}[[()]]]\n\
\[{[{({}]{}}([{[{{{}}([]\n\
\{<[[]]>}<{[{[{[]{()[[[]\n\
\[<(<(<(<{}))><([]([]()\n\
\<{([([[(<>()){}]>(<<{{\n\
\<{([{{}}[<[[[<>{}]]]>[]]"
testresult1 = 26397
testresult2 = 288957
test1 = test (solve1 . parse) testresult1 testdata
test2 = test (solve2 . parse) testresult2 testdata


main = do
    parsed <- parse <$> getInput
    putStr "Part 1: "
    print . solve1 $ parsed
    putStr "Part 2: "
    print . solve2 $ parsed
