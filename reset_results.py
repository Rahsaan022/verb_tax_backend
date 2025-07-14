import os
with open("results.csv", "w", encoding="utf-8") as f:
    f.write("prolific_pid,question_id,answer,confidence\n")
print("results.csv reset")
