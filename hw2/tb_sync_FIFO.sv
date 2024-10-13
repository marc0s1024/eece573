module tb_sync_FIFO;
    parameter SIZE = 4;
    parameter DEPTH = 16;
    logic clk_write, clk_read;
    logic [SIZE-1:0] data_in, data_out;
    logic empty, full;

    // inst sync_FIFO
    sync_FIFO #(.SIZE(SIZE), .DEPTH(DEPTH)) sync_FIFO_inst (
        .clk_write(clk_write),
        .clk_read(clk_read),
        .data_in(data_in),
        .data_out(data_out),
        .empty(empty),
        .full(full)
    );

    // gen clk
    initial begin
        clk_write = 0;
        forever #5 clk_write = ~clk_write; // toggle clk_write every 5 time units
    end

    initial begin
        clk_read = 0;
        forever #10 clk_read = ~clk_read; // toggle clk_read every 10 time units
    end

    // test FIFO
    initial begin

        // initial cond
        data_in = 4'b0000; 
        #10 // delay 10 time units

        // write data until fifo is full
        while (!full) begin
            data_in = data_in + 1; // increment data_in
            #10; // delay before next write
        end

        // read data until fifo is empty
        while (!empty) begin
            #10; // delay before next read
        end

        $finish;
    end
endmodule