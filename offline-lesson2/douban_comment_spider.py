import scrapy


class DoubanSpider(scrapy.Spider):
    name = "douban_comment"
    start_urls = [
        'https://movie.douban.com/subject/25894431/comments?status=P',
    ]

    def parse(self, response):
        for item in response.xpath('//div[@class="comment"]'):
            print item.xpath('//span[@class="votes pr5"]/text()').extract()[0]
            print item.xpath('//span[class="comment-info"]/a/text()').extract()[0]
            print item.xpath('//span[class="comment-info"]/a/@herf').extract()[0]
            print item.xpath('//span[@class="allstar30 rating"]/@title').extract()[0]
            print item.xpath('p/text()').extract()[0]
            print "\n"

            yield {
                'count_num': item.xpath('//span[@class="votes pr5"]/text()').extract()[0],
                'people': item.xpath('//span[class="comment-info"]/a/text()').extract()[0],
                'people_url': item.xpath('//span[class="comment-info"]/a/@herf').extract()[0],
                'star': item.xpath('//span[@class="allstar30 rating"]/@title').extract()[0],
                'comment': item.xpath('p/text()').extract()[0],
            }

