module sync_FIFO #(parameter SIZE = 4, DEPTH = 16) (
    input logic clk_write, clk_read, // input write and read clocks
    input logic [SIZE-1:0] data_in, // input data to write
    output logic [SIZE-1:0] data_out, // output data read
    output logic empty, full // output status of FIFO
);

    // FIFO memory
    logic [SIZE-1:0] fifo_memory [0:DEPTH-1];

    // write read ptrs
    logic [SIZE-1:0] write_ptr, read_ptr;
    logic [SIZE-1:0] write_ptr_gray, read_ptr_gray; 
    logic [SIZE-1:0] sync_write_ptr_gray, sync_read_ptr_gray;

    // inst write pointer_sync
    pointer_sync #(.SIZE(SIZE)) sync_write (
        .clk(clk_read),     // sync to read clock
        .bin_ptr_in(write_ptr), // input binary pointer
        .sync_gray_ptr_out(sync_write_ptr_gray) // output synced gray pointer
    )

    // inst read pointer_sync
    pointer_sync #(.SIZE(SIZE)) sync_read (
        .clk(clk_write),     // sync to write clock
        .bin_ptr_in(read_ptr), // input binary pointer
        .sync_gray_ptr_out(sync_read_ptr_gray) // output synced gray pointer
    )

    // detect when full
    assign full = (write_ptr == (read_ptr - 1));
    
    //detect when empty
    assign empty = (write_ptr == read_ptr);

    // write data
    always_ff @(posedge clk_write) begin
        fifo_memory[write_ptr] <= data_in; // write data to memory
        write_ptr <= write_ptr + 1; // increment write pointer
    end

    // read data
    always_ff @(posedge clk_read) begin
        if (!empty) begin
            data_out <= fifo_memory[read_ptr]; // read data from memory
            read_ptr <= read_ptr + 1; // increment read pointer
        end
    end
endmodule

