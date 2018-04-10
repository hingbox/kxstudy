#!/usr/bin/python
# -*- coding: utf-8 -*-


if __name__ == '__main__':
    data = [
        {"id":"1979254","title":"\\u524d\\u5546\\u52a1\\u90e8\\u5b98\\u5458:\\u8fd9\\u662f40\\u5e74\\u6765\\u7b2c\\u4e00\\u573a\\u771f\\u6b63\\u7684\\u4e2d\\u7f8e\\u8d38\\u6613\\u6218","media":"\\u65f6\\u4ee3\\u5468\\u62a5","author":"","comment_url":"","url":"http:\\/\\/finance.sina.com.cn\\/china\\/gncj\\/2018-04-10\\/doc-ifyvtmxe7692217.shtml","create_date":"2018-04-10","create_time":"04:00:15","cat_name":"finance_0_suda","top_time":"20180410","top_num":"36,072","ext1":"","ext2":"","ext3":"http:\\/\\/n.sinaimg.cn\\/news\\/crawl\\/72\\/w550h322\\/20180410\\/BDjJ-fyvtmxe7482560.jpg","ext4":"fyvtmxe7692217","ext5":"","time":"Tue, 10 Apr 2018 04:00:15 +0800"},
        {"id":"1979259","title":"\\u7279\\u6717\\u666e\\u6697\\u793a\\u53ef\\u80fd\\u4e0e\\u4e2d\\u56fd\\u5c31\\u8d38\\u6613\\u4e89\\u7aef\\u8fbe\\u6210\\u534f\\u8bae","media":"\\u65b0\\u6d6a\\u8d22\\u7ecf","author":"","comment_url":"","url":"http:\\/\\/finance.sina.com.cn\\/stock\\/usstock\\/c\\/2018-04-10\\/doc-ifyvtmxe7675230.shtml","create_date":"2018-04-10","create_time":"03:49:14","cat_name":"finance_0_suda","top_time":"20180410","top_num":"27,457","ext1":"","ext2":"","ext3":"http:\\/\\/n.sinaimg.cn\\/finance\\/transform\\/116\\/w550h366\\/20180410\\/75HT-fyvtmxe7671102.jpg","ext4":"fyvtmxe7675230","ext5":"","time":"Tue, 10 Apr 2018 03:49:14 +0800"},
        {"id":"1979261","title":"\\u4e60\\u8fd1\\u5e73\\uff1a\\u4e2d\\u56fd\\u5f00\\u653e\\u7684\\u5927\\u95e8\\u53ea\\u4f1a\\u8d8a\\u5f00\\u8d8a\\u5927\\uff08\\u65b0\\u653f\\u7b56\\u6c47\\u603b\\uff09","media":"\\u65b0\\u534e\\u793e","author":"","comment_url":"","url":"http:\\/\\/finance.sina.com.cn\\/china\\/2018-04-10\\/doc-ifyvtmxe8658276.shtml","create_date":"2018-04-10","create_time":"10:16:23","cat_name":"finance_0_suda","top_time":"20180410","top_num":"20,306","ext1":"","ext2":"","ext3":"","ext4":"fyvtmxe8658276","ext5":"","time":"Tue, 10 Apr 2018 10:16:23 +0800"},
        {"id":"1979270","title":"\\u6ef4\\u6ef4\\u53f8\\u673a\\u52a0\\u4ef7\\u4e0d\\u6210\\u9ad8\\u901f\\u7529\\u5ba2 \\u4e8b\\u540e\\u8c0e\\u79f0\\u4e58\\u5ba2\\u5438\\u6bd2\\u6253\\u53f8\\u673a","media":"\\u65b0\\u6d6a\\u7efc\\u5408","author":"","comment_url":"","url":"http:\\/\\/finance.sina.com.cn\\/consume\\/puguangtai\\/2018-04-10\\/doc-ifyvtmxe7974382.shtml","create_date":"2018-04-10","create_time":"07:15:21","cat_name":"finance_0_suda","top_time":"20180410","top_num":"13,982","ext1":"","ext2":"","ext3":"http:\\/\\/n.sinaimg.cn\\/front\\/732\\/w469h263\\/20180410\\/rtWo-fyvtmxe7974423.jpg","ext4":"fyvtmxe7974382","ext5":"","time":"Tue, 10 Apr 2018 07:15:21 +0800"}]

    for dd in data:
        d = []
        ss = dd['title'].replace('\\\\','\\')
        url = dd['url'].replace('\\', '')
        create_date = dd['create_date'].replace('\\', '')+" "+dd['create_time'].replace('\\', '')
        d.append(ss)
        d.append(url)
        d.append(create_date)
        print d
