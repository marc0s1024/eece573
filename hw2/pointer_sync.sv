module pointer_sync #(parameter SIZE = 4) (
    input logic clk,    // input clock
    input logic [SIZE-1:0] bin_ptr_in,  // input binary pointer
    output logic [SIZE-1:0] sync_gray_ptr_out,  // output synced gray pointer
);
    logic [SIZE-1:0] gray_ptr;  

    // inst bin2gray
    bin2gray #(.SIZE(SIZE)) bin2gray_inst (
        .bin(bin_ptr_in),
        .gray(gray_ptr)
    );

    // sync gray pointer
    always_ff @(posedge clk) begin
        sync_gray_ptr_out <= gray_ptr;
    end
endmodule