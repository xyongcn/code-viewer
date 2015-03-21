#! /usr/bin/ruby
require 'uri'
require 'net/http'
email = ARGV[0]
password = ARGV[1]
username = ARGV[2]
name = ARGV[3]
uri = URI.parse("http://south.cs.tsinghua.edu.cn/api/v3/users")
http = Net::HTTP::new(uri.host, uri.port)
request = Net::HTTP::Post.new(uri.request_uri)
request.set_form_data({"username" => username, "email" => email, "password" => password, "name" => name})
request["PRIVATE-TOKEN"] = "XXXXXXX"
response = http.request(request)
puts "#{response.body}"
