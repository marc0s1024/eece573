module sync_FIFO #(parameter SIZE = 4, DEPTH = 16) (
    input logic clk_write, clk_read, // input write and read clocks
    input logic reset,                  // reset signal for pointer initialization
    input logic [SIZE-1:0] data_in, // input data to write
    output logic [SIZE-1:0] data_out, // output data read
    output logic empty, full // output status of FIFO
);

    // FIFO memory
    logic [SIZE-1:0] fifo_memory [0:DEPTH-1];

    // write read ptrs
    logic [SIZE-1:0] write_ptr, read_ptr;
    logic [SIZE-1:0] old_write_ptr, old_read_ptr;
    logic [SIZE-1:0] write_ptr_gray, read_ptr_gray;
    logic [SIZE-1:0] sync_write_ptr, sync_read_ptr;
 
    // track write and read pointers
    always_ff @(posedge clk_write or posedge reset) begin
        if (reset) begin
            write_ptr <= 0;
            old_write_ptr <= 0;
        end 
        else begin
            old_write_ptr <= write_ptr;
            // if FIFO not full, update write pointer, write data to FIFO memory
            if (!full) begin
                fifo_memory[write_ptr] <= data_in;
                write_ptr <= write_ptr + 1;
            end
        end
    end

    always_ff @(posedge clk_read or posedge reset) begin
        if (reset) begin
            read_ptr <= 0;
            old_read_ptr <= 0;
        end 
        else begin
            old_read_ptr <= read_ptr;
            // if FIFO not empty, update read pointer, output data from FIFO memory
            if (!empty) begin
                data_out <= fifo_memory[read_ptr];
                read_ptr <= read_ptr + 1;
            end
        end
    end

    // set empty flag
    always_ff @(posedge clk_read or posedge reset) begin
        if (reset) begin
            empty <= 1'b1;
        end 
        else begin
            empty <= (write_ptr == read_ptr) && ((old_read_ptr + 1 == write_ptr) || empty);
        end
    end

    // set full flag
    always_ff @(posedge clk_write or posedge reset) begin
        if (reset) begin
            full <= 1'b0;
        end 
        else begin
            full <= (write_ptr == read_ptr) && ((old_write_ptr + 1 == read_ptr) || full);
        end
    end

    // convert write and read to gray and sync
    bin2gray #(SIZE) write_bin2gray (
        .bin(write_ptr),
        .gray(write_ptr_gray)
    );
    
    bin2gray #(SIZE) read_bin2gray (
        .bin(read_ptr),
        .gray(read_ptr_gray)
    );
    
    pointer_sync #(SIZE) sync_write (
        .clk(clk_read),
        .bin_ptr_in(write_ptr_gray),
        .sync_gray_ptr_out(sync_write_ptr)
    );
    
    pointer_sync #(SIZE) sync_read (
        .clk(clk_write),
        .bin_ptr_in(read_ptr_gray),
        .sync_gray_ptr_out(sync_read_ptr)
    );

endmodule