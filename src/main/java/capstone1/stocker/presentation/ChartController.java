package capstone1.stocker.presentation;

import capstone1.stocker.application.ChartService;
import capstone1.stocker.dto.ChartResponseDto;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/{tickerId}")
@Tag(name = "Chart Controller", description = "차트 컨트롤러")
@RequiredArgsConstructor
@Slf4j
public class ChartController {
    private final ChartService chartService;

    @GetMapping
    @Operation(summary = "차트 정보를 조회", description = "종목코드에 해당하는 종목의 3개월 주식 차트를 조회")
    @ApiResponses({
            @ApiResponse(responseCode = "200", description = "차트 조회 성공"),
            @ApiResponse(responseCode = "404", description = "존재하지 않는 종목코드"),
            @ApiResponse(responseCode = "500", description = "잘못된 요청 정보")
    })
    public ResponseEntity<ChartResponseDto> chartDetail(@PathVariable String tickerId)
            throws Exception {
        log.info("tickerId : {}" , tickerId);
        return ResponseEntity.ok(chartService.getChart(tickerId));
    }
}
