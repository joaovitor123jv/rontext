require 'socket'

APPLICATION_KEY = "CTXTSEARCH"

class Server
    def initialize(port)
        @port = port
        @server = TCPServer.open(port)
    end

    def listen
        loop do
            Thread.start(@server.accept) do |client|
                puts "CLIENT CONNECTED"
                if client.gets.chomp == APPLICATION_KEY
                    puts "KEY ACCEPTED"
                    yield(client)
                else
                    client.puts "ERROR, WRONG KEY"
                    client.close
                end
            end
        end
    end
end
