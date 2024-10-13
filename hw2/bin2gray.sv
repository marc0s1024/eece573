module bin2gray #(parameter SIZE = 4) (
    input logic [SIZE-1:0] bin,
    output logic [SIZE-1:0] gray
);
    always_comb begin
       gray = (bin >> 1) ^ bin;
    end
endmodule