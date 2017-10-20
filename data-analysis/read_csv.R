csv = read.csv("C:/Users/admin/Downloads/CXR_4873_1020152220.csv", encoding = "utf-8")

csv$店仓 = gsub("=","",csv$店仓)
csv$店名 = gsub("=","",csv$店名)
csv$单据日期 = gsub("=","",csv$单据日期)
csv$商品 = gsub("=","",csv$商品)
csv$商品名称 = gsub("=","",csv$商品名称)
csv$大类 = gsub("=","",csv$大类)
csv$条码.颜色= gsub("=","",csv$条码.颜色)
csv$年份= gsub("=","",csv$年份)
csv$折扣...= gsub("=","",csv$折扣...)
csv$备注= gsub("=","",csv$备注)
csv$单据日期.当年第几天= gsub("=","",csv$单据日期.当年第几天)

csv$单据日期 = as.Date(csv$单据日期,"%Y%m%d")

View(csv)
str(csv)
summary(csv)

#每日成交
table.day_sum = aggregate(csv$成交金额,by=list(Day=csv$单据日期), FUN=sum)  
plot(table.day_sum, type='l', col = "red")