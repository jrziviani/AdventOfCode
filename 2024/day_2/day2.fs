open System.IO

type Level = int list
type Report = Level list

let report = [
    [7; 6; 4; 2; 1];
    [1; 2; 7; 8; 9];
    [9; 7; 6; 2; 1];
    [1; 3; 2; 4; 5];
    [8; 6; 4; 4; 1];
    [1; 3; 6; 7; 9]
]

let readFileToReport (path: string): Report =
    File.ReadAllLines(path)
    |> Array.map (fun line ->
        line.Split(' ')
        |> Array.map int
        |> Array.toList)
    |> Array.toList

let rec CheckSafety (level: Level) =
    match level with
    | [] | [_] -> true
    | a::b::tail -> match abs(a - b) with
                    | 1 | 2 | 3 -> CheckSafety (b::tail)
                    | _ -> false

let rec IsSingleDirection (op: int -> int -> bool) (level: Level) =
    match level with
    | [] | [_] -> true
    | a::b::tail -> if op a b
                    then IsSingleDirection op (b::tail)
                    else false

let IsReportSafePartI (report: Report) =
    report
    |> List.filter (fun level -> IsSingleDirection (>) level || IsSingleDirection (<) level)
    |> List.filter CheckSafety
    |> List.length

let IsReportSafePartII (report: Report) =
    let rec IsSafe (level: Level) =
        [0..(level.Length - 1)]
        |> List.map (fun i -> level.[0..(i - 1)] @ level.[(i + 1)..(level.Length - 1)])
        |> List.filter (fun elem -> IsSingleDirection (>) elem || IsSingleDirection (<) elem)
        |> List.filter CheckSafety
        |> List.length > 0

    report
    |> List.filter IsSafe
    |> List.length

[<EntryPoint>]
let main args =
    if args.Length <> 1
    then printfn "Usage: Program.exe <input path>"
    else
        let path = args[0]
        let numbers = readFileToReport path
        printfn "Safe reports I: %d" (IsReportSafePartI numbers)
        printfn "Safe reports II: %d" (IsReportSafePartII numbers)
    0
