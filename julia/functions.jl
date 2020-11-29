function work(x)
    x * 2
end

work_single_line(x) = x+5
passed = work_single_line


println(work(4))
println(work_single_line(20))
println(passed(25))