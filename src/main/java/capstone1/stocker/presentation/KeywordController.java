package capstone1.stocker.presentation;

import capstone1.stocker.application.KeywordService;
import capstone1.stocker.dto.KeywordResponseDto;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@Tag(name = "Keyword Controller", description = "키워드 컨트롤러")
@RequestMapping("/tickers/{ticker}")
@RequiredArgsConstructor
public class KeywordController {
    private final KeywordService keywordService;


    @GetMapping("/keywords")
    @Operation(summary = "모든 키워드를 조회합니다.", description = "종목에 해당하는 존재하는 모든 키워드를 조회합니다")
    public ResponseEntity<KeywordResponseDto> keywordList(@PathVariable String ticker){
        KeywordResponseDto result = keywordService.readAllKeywordByCompany(ticker);
        return ResponseEntity.ok(result);
    }


}
