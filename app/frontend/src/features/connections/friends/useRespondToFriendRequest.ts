import { Empty } from "google-protobuf/google/protobuf/empty_pb";
import { Error } from "grpc-web";
import { friendRequestKey } from "queryKeys";
import { useMutation, useQueryClient } from "react-query";
import { service } from "service";

import { SetMutationError } from ".";

interface RespondToFriendRequestVariables {
  accept: boolean;
  friendRequestId: number;
  setMutationError: SetMutationError;
}

export default function useRespondToFriendRequest() {
  const queryClient = useQueryClient();
  const {
    mutate: respondToFriendRequest,
    isLoading,
    isSuccess,
    reset,
  } = useMutation<Empty, Error, RespondToFriendRequestVariables>(
    ({ friendRequestId, accept }) =>
      service.api.respondFriendRequest(friendRequestId, accept),
    {
      onError: (error, { setMutationError }) => {
        setMutationError(error.message);
      },
      onMutate: async ({ setMutationError }) => {
        setMutationError("");
        await queryClient.cancelQueries(friendRequestKey("received"));
      },
      onSuccess: () => {
        queryClient.invalidateQueries("friendIds");
        queryClient.invalidateQueries(friendRequestKey("received"));
        queryClient.invalidateQueries("ping");
      },
    }
  );

  return { isLoading, isSuccess, reset, respondToFriendRequest };
}
