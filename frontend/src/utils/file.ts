export default class{
    static dataURLtoFile(dataurl:string, filename:string) {
        console.log(dataurl)
        var arr = dataurl.split(',');
        var result:string = "";
        if(arr!=null){
            var mimex = arr[0].match(/:(.*?);/)
            if(mimex!=null){
                result = mimex[1]
            }
        }
        var bstr = atob(arr[1])
        var n = bstr.length
        var u8arr = new Uint8Array(n);
        console.log(arr)
        console.log(bstr)
        while(n--){
            u8arr[n] = bstr.charCodeAt(n);
        }
        let r=new File([u8arr], filename, {type:result})
        console.log(r)
        return new File([u8arr], filename, {type:result});
    }
}