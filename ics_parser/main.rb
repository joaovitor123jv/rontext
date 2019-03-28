require 'icalendar'
require './server.rb'

port = 2000

server = Server.new(port)
puts "ICS PARSER STARTED"

server.listen do |client|
    puts "ICS PARSER LISTENING"
    file_name = client.gets.chomp
    if File.exist? file_name
        client.puts "FILE EXISTS"

        cal_file = File.open(file_name)
        cals = Icalendar::Calendar.parse(cal_file)

        cal = cals.first
        event = cal.events.first

        puts "start date-time: #{event.dtstart}"
        puts "start date-time timezone: #{event.dtstart.ical_params['tzid']}"
        puts "summary: #{event.summary}"

        client.puts "EVENT SUMMARY == #{event.summary}"

    else
        client.puts "ERROR: Invalid filename"
    end
end