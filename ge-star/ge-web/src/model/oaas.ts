import {grpc} from "@improbable-eng/grpc-web";

export type ServiceError = { message: string, code: number; metadata: grpc.Metadata }
export type Status = { details: string, code: number; metadata: grpc.Metadata }

interface UnaryResponse {
    cancel(): void;
}

interface ResponseStream<T> {
    cancel(): void;
    on(type: 'data', handler: (message: T) => void): ResponseStream<T>;
    on(type: 'end', handler: (status?: Status) => void): ResponseStream<T>;
    on(type: 'status', handler: (status: Status) => void): ResponseStream<T>;
}

interface RequestStream<T> {
    write(message: T): RequestStream<T>;
    end(): void;
    cancel(): void;
    on(type: 'end', handler: (status?: Status) => void): RequestStream<T>;
    on(type: 'status', handler: (status: Status) => void): RequestStream<T>;
}

interface BidirectionalStream<ReqT, ResT> {
    write(message: ReqT): BidirectionalStream<ReqT, ResT>;
    end(): void;
    cancel(): void;
    on(type: 'data', handler: (message: ResT) => void): BidirectionalStream<ReqT, ResT>;
    on(type: 'end', handler: (status?: Status) => void): BidirectionalStream<ReqT, ResT>;
    on(type: 'status', handler: (status: Status) => void): BidirectionalStream<ReqT, ResT>;
}


/**
 * A metadata builder to simplify the grpc calls.
 */
export class MetadataManager {
    static get(): grpc.Metadata {
        const metadata = new grpc.Metadata({
            'x-oaas-auth': 'abcd',
            'x-oaas-route': JSON.stringify({
                'custom': 'structure',
                'is': ['here']
            })
        });

        return metadata;
    }
}


export function client<T>(type: new(s: string) => T, tags: object|null = null): T {
    return new type("http://localhost:9000")
}


/**
 * Transform a single grpc call into a promise.
 */
export function asPromise<S, R>(
    that: any,
    fn: (data: S, callback: (err: ServiceError|null, resp: R|null) => void) => UnaryResponse,
): (data: S) => Promise<R> {
// S=sent, R=response, UR=unary response
    function _call(data: S): Promise<R> {
        return new Promise((resolve, reject) => {
            const args: any = [data]

            args.push((err: Error|null, result: R) => {
                if (err) {
                    reject(err);
                    return;
                }

                resolve(result);
            })

            fn.apply(that, args)
        });
    }

    return _call;
}


/**
 * Transforms a single grpc call, with optional metadata into a promise.
 * @param that
 * @param fn
 */
export function asPromiseWithMetadata<S, R>(
    that: any,
    fn: (data: S, metadata: grpc.Metadata, callback: (err: ServiceError|null, resp: R|null) => void) => UnaryResponse,
): (data: S, metadata: grpc.Metadata) => Promise<R> {
// S=sent, R=response, UR=unary response
    function _call(data: S, metadata: grpc.Metadata|null): Promise<R> {
        return new Promise((resolve, reject) => {
            const args: any = [data, metadata]

            args.push((err: Error|null, result: R) => {
                if (err) {
                    reject(err);
                    return;
                }

                resolve(result);
            })

            fn.apply(that, args)
        });
    }

    return _call;
}
