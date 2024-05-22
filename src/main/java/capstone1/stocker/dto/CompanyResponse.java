package capstone1.stocker.dto;

import java.util.HashMap;
import java.util.Map;

public record CompanyResponse (
    Map <String,String> tickers
) {
    public static CompanyResponse from(HashMap result){
        return new CompanyResponse(result);
    }
}
