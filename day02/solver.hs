import Data.List
import Utils

getInput :: IO String
getInput = do
    contents <- readFile "input.txt"
    return contents


type Parsed = [(String, Int)]
type Sol1 = Int
type Sol2 = Int



parse :: String -> Parsed
parse = map parseInstruction . map words . lines
    where
        parseInstruction (dir:x:[]) = (dir, read x)


move :: (Int, Int) -> (String, Int) -> (Int, Int)
move (x, d) ("forward", dx) = (x + dx, d)
move (x, d) ("down", dd)    = (x, d + dd)
move (x, d) ("up", dd)      = (x, d - dd)


solve1 :: Parsed -> Sol1
solve1 parsed = x * d
    where
        (x, d) = foldl move (0, 0) parsed


solve2 :: Parsed -> Sol2
solve2 parsed = undefined


testdata = "forward 5\n\
\down 5\n\
\forward 8\n\
\up 3\n\
\down 8\n\
\forward 2"
testresult1 = 150
testresult2 = 0
test1 = test (solve1 . parse) testresult1 testdata
test2 = test (solve2 . parse) testresult2 testdata


main = do
    parsed <- parse <$> getInput
    putStr "Part 1: "
    print . solve1 $ parsed
    putStr "Part 2: "
    print . solve2 $ parsed
