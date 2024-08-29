seconds = 5555
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
formatted_time = "%02d:%02d:%02d" % (h, m, s)
print(formatted_time)
