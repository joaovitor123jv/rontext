#!/usr/bin/ruby
args = ARGV

require "rb-inotify"

def startListener(path)
    notifier = INotify::Notifier.new

    notifier.watch(path, :modify) { |file|
        puts "#{file.name} was modified"
    }

    notifier.watch(path, :moved_to, :create) { |file|
        puts "#{file.name} was moved or created"
    }

    notifier.run
end

if args.first.nil?
    puts "Starting File System Listener on #{ENV['HOME']}"
    startListener(ENV['HOME'])
elsif args.first == "increase-inotify-limit"
    system "echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p"
elsif( File.exist?(args.first) )
    if( File.directory?(args.first) )
        puts "Starting File System Listener on #{args.first}"
        startListener(args.first)
    else
        puts "Please, give me a directory, instead of any other thing"
    end
else
    puts "Invalid argument, please informa a directory or 'increase-inotify-limit' as arguments"
end
