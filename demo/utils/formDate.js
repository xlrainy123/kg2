/**
 * \[TimeToDate时间戳转换为日期\]
 * @param {\[type\]} unixTime \[时间戳\]
 * @param {String} type     \[Y-m-d,Y-m-d H:i:s,Y/m/d,Y/m/d H:i:s,Y年m月d日,Y年m月d日 H:i:s\]
 */
function TimeToDate(unixTime,type="Y-M-D H:i:s"){
    var date = new Date(unixTime);//时间戳为10位需*1000，时间戳为13位的话不需乘1000
    var datetime = "";
    datetime += date.getFullYear() + type.substring(1,2);
    datetime += (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + type.substring(3,4);
    datetime += (date.getDate() < 10 ? '0'+(date.getDate()) : date.getDate());
    if (type.substring(5,6)) {
        if (type.substring(5,6).charCodeAt() > 255) {
            datetime += type.substring(5,6);
            if (type.substring(7,8)) {
                datetime += " " + (date.getHours() < 10 ? '0'+(date.getHours()) : date.getHours());
                if (type.substring(9,10)) {
                    datetime += type.substring(8,9) + (date.getMinutes() < 10 ? '0'+(date.getMinutes()) : date.getMinutes());
                    if (type.substring(11,12)) {
                        datetime += type.substring(10,11) + (date.getSeconds() < 10 ? '0'+(date.getSeconds()) : date.getSeconds());
                    };
                };
            };
        }else{
            datetime += " " + (date.getHours() < 10 ? '0'+(date.getHours()) : date.getHours());
            if (type.substring(8,9)) {
                datetime += type.substring(7,8) + (date.getMinutes() < 10 ? '0'+(date.getMinutes()) : date.getMinutes());
                if (type.substring(10,11)) {
                    datetime += type.substring(9,10) + (date.getSeconds() < 10 ? '0'+(date.getSeconds()) : date.getSeconds());
                };
            };
        };
    };
    return datetime;
}
