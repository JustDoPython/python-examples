hostname_dic = {}
with open("chrome_history.csv", encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile)
    birth_header = next(csv_reader)
    for row in csv_reader:
        hostname = parse.urlparse(row[0]).hostname
        hostname_dic[hostname] = hostname_dic.get(hostname, 0) + 1
sorted(hostname_dic.items(),key = lambda x:x[1],reverse = True)


c = (
    Pie()
    .add(
        "",
        [
            list(z)
            for z in zip(
                list(hostname_dic)[0:10],
                list(hostname_dic.values())[0:10],
            )
        ],
        center=["40%", "50%"],
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="历史记录"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
    )
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    .render("pie_scroll_legend.html")
)
        
print(hostname_dic)
