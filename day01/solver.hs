import Data.List
import Utils

getInput :: IO String
getInput = do
    contents <- readFile "input.txt"
    return contents


type Parsed = [Int]
type Sol1 = Int
type Sol2 = Int



parse :: String -> Parsed
parse = parseInts


solve1 :: Parsed -> Sol1
solve1 = length . filter (>0) . diff


solve2 :: Parsed -> Sol2
solve2 = length . filter (>0) . diff . map sum . Utils.slidingWindow 3


testdata = "199\n\
\200\n\
\208\n\
\210\n\
\200\n\
\207\n\
\240\n\
\269\n\
\260\n\
\263\n"
testresult1 = 7
testresult2 = 5
test1 = test (solve1 . parse) testresult1 testdata
test2 = test (solve2 . parse) testresult2 testdata


main = do
    parsed <- parse <$> getInput
    putStr "Part 1: "
    print . solve1 $ parsed
    putStr "Part 2: "
    print . solve2 $ parsed
