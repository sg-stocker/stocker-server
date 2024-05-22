package capstone1.stocker.presentation;

import capstone1.stocker.application.CompanyService;
import capstone1.stocker.dto.CompanyResponse;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import java.util.HashMap;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/tickers")
@Tag(name = "Company Controller", description = "회사 컨트롤러")
@RequiredArgsConstructor
public class CompanyController {
    private final CompanyService companyService;

    @GetMapping
    @Operation(summary = "전체 회사를 전부 조회", description = "사용 가능한 회사들을 전부 조회한다")
    @ApiResponse(responseCode = "200" , description = "전체 조회 성공")
    public ResponseEntity<HashMap> companyList(){
        return ResponseEntity.ok(companyService.getAllCompanies());
    }
}
