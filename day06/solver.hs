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
parse = Utils.parseInts


step :: [Int] -> [Int]
step (n0:n1:n2:n3:n4:n5:n6:n7:n8:[]) = n1:n2:n3:n4:n5:n6:(n7+n0):n8:n0:[]

life :: Int -> [Int] -> [Int]
life 0 fish = fish
life d fish = life (d-1) (step fish)


fish :: Parsed -> [Int]
fish parsed = [length . filter (==i) $ parsed | i <- [0..8]]


solve1 :: Parsed -> Sol1
solve1 = sum . life 80 . fish


solve2 :: Parsed -> Sol2
solve2 = sum . life 256 . fish


testdata = "3,4,3,1,2"
testresult1 = 5934
testresult2 = 26984457539
test1 = test (solve1 . parse) testresult1 testdata
test2 = test (solve2 . parse) testresult2 testdata


main = do
    parsed <- parse <$> getInput
    putStr "Part 1: "
    print . solve1 $ parsed
    putStr "Part 2: "
    print . solve2 $ parsed
